""" ============== Cart Models (Improved) =============== """
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, Region, City
from apps.products.models import Product, ProductVariant
from apps.utilities.models import BaseModel
from apps.users.models import User


# ============== Cart Model ===============
class Cart(BaseModel):
    """
    Shopping Cart Model - Supports both authenticated and guest users
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="carts",
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    
    # For guest users
    session_key = models.CharField(
        max_length=40, 
        blank=True, 
        null=True,
        db_index=True,
        verbose_name=_("Session Key"),
        help_text=_("Session key for guest users")
    )
    
    # Cart status
    class CartStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        ABANDONED = "abandoned", _("Abandoned")
        CONVERTED = "converted", _("Converted to Order")
    
    status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
        verbose_name=_("Status")
    )
    
    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["session_key", "status"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        if self.user:
            return f"Cart #{self.id} - {self.user.email}"
        return f"Cart #{self.id} - Guest ({self.session_key})"
    
    @property
    def total_items(self):
        """Total number of items in cart"""
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def subtotal(self):
        """Subtotal of all items"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def is_empty(self):
        """Check if cart is empty"""
        return self.total_items == 0
    
    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()
    
    def merge_with(self, other_cart):
        """Merge another cart into this cart"""
        if not other_cart:
            return
        
        for item in other_cart.items.all():
            # Check if item already exists in this cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=self,
                product=item.product,
                variant=item.variant,
                defaults={
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                }
            )
            if not created:
                # Update quantity if already exists
                cart_item.quantity += item.quantity
                cart_item.save()
        
        # Delete the old cart
        other_cart.delete()
    
    @classmethod
    def get_or_create_cart(cls, user=None, session_key=None):
        """Get or create active cart for user/session"""
        # Authenticated user
        if user and user.is_authenticated:
            cart, created = cls.objects.get_or_create(
                user=user,
                status=cls.CartStatus.ACTIVE,
                defaults={'session_key': session_key}
            )
            
            # Merge guest cart if exists
            if session_key and not created:
                guest_cart = cls.objects.filter(
                    session_key=session_key,
                    status=cls.CartStatus.ACTIVE,
                    user__isnull=True
                ).first()
                if guest_cart:
                    cart.merge_with(guest_cart)
            
            return cart
        
        # Guest user
        elif session_key:
            cart, created = cls.objects.get_or_create(
                session_key=session_key,
                status=cls.CartStatus.ACTIVE,
                user__isnull=True
            )
            return cart
        
        return None


# ============== Cart Item Model ===============
class CartItem(BaseModel):
    """Individual items in shopping cart"""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name="items",
        verbose_name=_("Cart")
    )
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name="cart_items",
        verbose_name=_("Product")
    )
    
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cart_items",
        verbose_name=_("Variant"),
        help_text=_("Product variant (if any)")
    )
    
    product_name = models.CharField(
        max_length=255,
        verbose_name=_("Product Name"),
        help_text=_("Snapshot of product name at add time")
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantity")
    )
    
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name=_("Unit Price"),
        help_text=_("Snapshot of price at add time")
    )
    
    class Meta:
        unique_together = ("cart", "product", "variant")
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        indexes = [
            models.Index(fields=["cart", "product"]),
            models.Index(fields=["cart", "variant"]),
        ]

    def __str__(self):
        variant_text = f" ({self.variant})" if self.variant else ""
        return f"{self.product_name}{variant_text} x {self.quantity}"
    
    def clean(self):
        """Validate cart item before saving"""
        # Check if variant belongs to product
        if self.variant and self.variant.product != self.product:
            raise ValidationError({
                'variant': _("Variant doesn't belong to the selected product")
            })
        
        # Check stock availability
        if self.variant and hasattr(self.variant, 'track_inventory') and self.variant.track_inventory:
            if self.quantity > self.variant.stock_quantity:
                raise ValidationError({
                    'quantity': _(f"Only {self.variant.stock_quantity} items available in stock")
                })
        elif hasattr(self.product, 'track_inventory') and self.product.track_inventory:
            if self.quantity > self.product.stock_quantity:
                raise ValidationError({
                    'quantity': _(f"Only {self.product.stock_quantity} items available in stock")
                })
    
    def save(self, *args, **kwargs):
        """Auto-populate product_name and price before saving"""
        # Set product_name if not provided
        if not self.product_name:
            self.product_name = self.product.title if hasattr(self.product, 'title') else str(self.product)
        
        # Set price if not provided
        if not self.price:
            if self.variant:
                self.price = self.variant.price
            else:
                self.price = self.product.price if hasattr(self.product, 'price') else 0
        
        # Validate before saving
        self.clean()
        
        super().save(*args, **kwargs)
    
    @property
    def total_price(self):
        """Calculate total price for this item"""
        return self.quantity * self.price
    
    @property
    def available_stock(self):
        """Get available stock for this item"""
        if self.variant and hasattr(self.variant, 'stock_quantity'):
            return self.variant.stock_quantity
        elif hasattr(self.product, 'stock_quantity'):
            return self.product.stock_quantity
        return 999
    
    def increase_quantity(self, amount=1):
        """Increase quantity"""
        self.quantity += amount
        self.save()
    
    def decrease_quantity(self, amount=1):
        """Decrease quantity"""
        if self.quantity > amount:
            self.quantity -= amount
            self.save()
        else:
            self.delete()


# ============== Shipping Address Model ===============
class ShippingAddress(BaseModel):
    """Shipping address for order delivery"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="shipping_addresses",
        verbose_name=_("User")
    )
    
    full_name = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name=_("Full Name")
    )
    
    phone_number = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name=_("Phone Number")
    )
    
    street_address = models.TextField(
        blank=True,
        verbose_name=_("Street Address")
    )
    
    country = models.ForeignKey(
        Country, 
        on_delete=models.CASCADE, 
        related_name="shipping_addresses",
        verbose_name=_("Country")
    )
    
    province = models.ForeignKey(
        Region, 
        on_delete=models.CASCADE, 
        related_name="shipping_addresses", 
        null=True, 
        blank=True,
        verbose_name=_("Province/State")
    )
    
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name="shipping_addresses", 
        null=True, 
        blank=True,
        verbose_name=_("City")
    )
    
    postal_code = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name=_("Postal Code")
    )
    
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default Address")
    )
    
    # Additional helpful fields
    address_type = models.CharField(
        max_length=20,
        choices=[
            ('home', _('Home')),
            ('work', _('Work')),
            ('other', _('Other')),
        ],
        default='home',
        verbose_name=_("Address Type")
    )
    
    landmark = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Landmark"),
        help_text=_("Nearby landmark for easy identification")
    )
    
    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")
        ordering = ["-is_default", "-created_at"]
        indexes = [
            models.Index(fields=["user", "is_default"]),
            models.Index(fields=["user", "address_type"]),
        ]

    def __str__(self):
        name = self.full_name or self.user.email
        address_preview = self.street_address[:20] if self.street_address else "No address"
        return f"{name} - {address_preview}"
    
    def save(self, *args, **kwargs):
        """Ensure only one default address per user"""
        if self.is_default:
            ShippingAddress.objects.filter(
                user=self.user, 
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
    
    def get_full_address(self):
        """Get complete formatted address"""
        parts = []
        
        if self.full_name:
            parts.append(self.full_name)
        
        if self.street_address:
            parts.append(self.street_address)
        
        city_parts = []
        if self.city:
            city_parts.append(self.city.name)
        if self.province:
            city_parts.append(self.province.name)
        if city_parts:
            parts.append(", ".join(city_parts))
        
        if self.country:
            parts.append(self.country.name)
        
        if self.postal_code:
            parts.append(self.postal_code)
        
        if self.landmark:
            parts.append(f"(Near: {self.landmark})")
        
        if self.phone_number:
            parts.append(f"Tel: {self.phone_number}")
        
        return "\n".join(parts)
    
    def get_full_address_single_line(self):
        """Get address in single line"""
        return self.get_full_address().replace("\n", ", ")


# ============== Deprecated Address Model (Remove later) ===============
class Address(BaseModel):
    """DEPRECATED: This model is deprecated. Use ShippingAddress instead."""
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Address (Deprecated)")
        verbose_name_plural = _("Addresses (Deprecated)")
    
    def __str__(self):
        return self.street