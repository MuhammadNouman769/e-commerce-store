"""
================================================================================
    CART MODELS BTR Mall Shopping Cart
    Purpose: Shopping cart management for authenticated and guest users
    Author: Muhammad Nouman
================================================================================
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, Region, City
from apps.utils.models import BaseModel
from apps.products.models import Product, ProductVariant

'''
 ==================================================================================
  1. CART MODEL IMPLEMENTATION
    Purpose: Shopping cart management for authenticated and guest users
      Features:
        - User (ForeignKey to User model) - the user who owns the cart
        - Session key (CharField) - the session key for guest users
        - Status (CharField) - the status of the cart (active, abandoned, converted to order)
        - Coupon code (CharField) - the coupon code applied to the cart
        - Discount amount (DecimalField) - the discount amount applied to the cart
=================================================================================
 '''
class Cart(BaseModel):
    """Shopping Cart Model - supports both authenticated and guest users"""
    class CartStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        ABANDONED = "abandoned", _("Abandoned")
        CONVERTED = "converted", _("Converted to Order")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True,
        verbose_name=_("User"),
        help_text=_("Authenticated user (null for guest users)")
    )
    
    session_key = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        db_index=True,
        verbose_name=_("Session Key"),
        help_text=_("Django session key for guest users")
    )
    
    status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
        verbose_name=_("Status")
    )
    
    coupon_code = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name=_("Coupon Code")
    )
    discount_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name=_("Discount Amount")
    )

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        indexes = [
            models.Index(
                fields=["user", "status"], 
                name="cart_user_status_idx"
            ),
            models.Index(
                fields=["session_key", "status"], 
                name="cart_session_status_idx"
            ),
            models.Index(
                fields=["-created_at"], 
                name="cart_created_at_idx"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cart #{self.id} - {self.user.email}" if self.user else f"Cart #{self.id} - Guest ({self.session_key})"

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total(self):
        return self.subtotal - self.discount_amount

    @property
    def is_empty(self):
        return self.total_items == 0

    def clear(self):
        self.items.all().delete()

    def merge_with(self, other_cart):
        if not other_cart or other_cart == self:
            return
        for item in other_cart.items.all():
            cart_item, created = CartItem.objects.get_or_create(
                cart=self,
                product=item.product,
                variant=item.variant,
                defaults={
                    "product_name": item.product_name,
                    "variant_name": item.variant_name,
                    "sku": item.sku,
                    "quantity": item.quantity,
                    "price": item.price,
                }
            )
            if not created:
                cart_item.quantity += item.quantity
                cart_item.save()
        other_cart.delete()

    def apply_coupon(self, coupon_code, discount_amount):
        self.coupon_code = coupon_code
        self.discount_amount = discount_amount
        self.save()

    def remove_coupon(self):
        self.coupon_code = ""
        self.discount_amount = 0
        self.save()

    @classmethod
    def get_or_create_cart(cls, user=None, session_key=None):
        if user and user.is_authenticated:
            cart, created = cls.objects.get_or_create(
                user=user, 
                status=cls.CartStatus.ACTIVE, 
                defaults={'session_key': session_key}
            )
            if session_key and not created:
                guest_cart = cls.objects.filter(
                    session_key=session_key, 
                    status=cls.CartStatus.ACTIVE, 
                    user__isnull=True
                ).first()
                if guest_cart and not guest_cart.is_empty:
                    cart.merge_with(guest_cart)
            return cart
        elif session_key:
            cart, _ = cls.objects.get_or_create(
                session_key=session_key, 
                status=cls.CartStatus.ACTIVE, 
                user__isnull=True
            )
            return cart
        return None


'''
=================================================================================
  2. CART ITEM MODEL IMPLEMENTATION
      Purpose: Individual items in shopping cart
      Features:
        - Cart (ForeignKey to Cart model) - the cart this item belongs to
        - Product (ForeignKey to Product model) - the product in this item
        - Variant (ForeignKey to ProductVariant model) - the variant in this item
        - Product name (CharField) - the name of the product
        - Variant name (CharField) - the name of the variant
        - SKU (CharField) - the SKU of the product
        - Quantity (PositiveIntegerField) - the quantity of the product
        - Price (DecimalField) - the price of the product
=================================================================================
 '''
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
        verbose_name=_("Variant")
    )

    product_name = models.CharField(
        max_length=255, 
        verbose_name=_("Product Name")
    )
    variant_name = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name=_("Variant Name")
    )
    sku = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name=_("SKU")
    )
    quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name=_("Quantity")
    )
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name=_("Unit Price")
    )

    class Meta:
        unique_together = ("cart", "product", "variant")
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        indexes = [
            models.Index(
                fields=["cart", "product"], 
                name="cartitem_cart_product_idx"
            ),
            models.Index(
                fields=["cart", "variant"], 
                name="cartitem_cart_variant_idx"
            ),
        ]

    def __str__(self):
        variant_text = f" ({self.variant_name})" if self.variant_name else ""
        return f"{self.product_name}{variant_text} x {self.quantity}"

    def clean(self):
        if self.variant and self.variant.product != self.product:
            raise ValidationError(
                {"variant": _("Variant doesn't belong to selected product")}
            )
        if self.variant and self.variant.track_inventory and self.quantity > self.variant.stock_quantity:
            raise ValidationError(
                {"quantity": _(f"Only {self.variant.stock_quantity} items available")}
            )
        elif self.product.track_inventory and not self.variant and self.quantity > self.product.stock_quantity:
            raise ValidationError(
                {"quantity": _(f"Only {self.product.stock_quantity} items available")}
            )

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.title
        if self.variant and not self.variant_name:
            self.variant_name = self.variant.get_variant_name() or ""
        if not self.sku:
            if self.variant and self.variant.sku:
                self.sku = self.variant.sku
            elif self.product.sku:
                self.sku = self.product.sku
        if not self.price:
            self.price = self.variant.price if self.variant else self.product.price or 0
        self.clean()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity * self.price

    @property
    def available_stock(self):
        if self.variant and self.variant.track_inventory:
            return self.variant.stock_quantity
        elif self.product.track_inventory and not self.variant:
            return self.product.stock_quantity
        return 999


'''
=================================================================================
  3. SHIPPING ADDRESS MODEL IMPLEMENTATION
       Purpose: User shipping addresses
      Features:
        - User (ForeignKey to User model) - the user who owns the address
        - Address type (CharField) - the type of the address (home, work, other)
        - Full name (CharField) - the full name of the user
        - Phone number (CharField) - the phone number of the user
        - Alternate phone (CharField) - the alternate phone number of the user
        - Street address (TextField) - the street address of the user
        - Landmark (CharField) - the landmark of the user
        - Country (ForeignKey to Country model) - the country of the user
        - Province (ForeignKey to Region model) - the province of the user
        - City (ForeignKey to City model) - the city of the user
        - Postal code (CharField) - the postal code of the user
        - Is default (BooleanField) - whether the address is the default address
=================================================================================
 '''
class ShippingAddress(BaseModel):
    """User shipping addresses"""
    class AddressType(models.TextChoices):
        HOME = "home", _("Home")
        WORK = "work", _("Work")
        OTHER = "other", _("Other")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="shipping_addresses", 
        verbose_name=_("User")
    )
    address_type = models.CharField(
        max_length=20, 
        choices=AddressType.choices, 
        default=AddressType.HOME, 
        verbose_name=_("Address Type")
    )

    full_name = models.CharField(
        max_length=255, 
        verbose_name=_("Full Name")
    )
    phone_number = models.CharField(
        max_length=20, 
        verbose_name=_("Phone Number")
    )
    alternate_phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_("Alternate Phone")
    )

    street_address = models.TextField(
        verbose_name=_("Street Address")
    )
    landmark = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name=_("Landmark")
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

    class Meta:
        verbose_name = _(
            "Shipping Address"
        )
        verbose_name_plural = _(
            "Shipping Addresses"
        )
        ordering = [
            "-is_default", 
            "-created_at"
        ]
        indexes = [
            models.Index(
                fields=["user", "is_default"], 
                name="address_user_default_idx"
            ),
            models.Index(
                fields=["user", "address_type"], 
                name="address_user_type_idx"
            ),
        ]

    def __str__(self):
        city_name = self.city.name if self.city else "Unknown"
        return f"{self.full_name} - {city_name}"

    def save(self, *args, **kwargs):
        if self.is_default:
            ShippingAddress.objects.filter(
                user=self.user, 
                is_default=True
            ).exclude(
                pk=self.pk
            ).update(
                is_default=False
            )
        super().save(*args, **kwargs)

    def get_full_address(self):
        parts = [
            self.full_name, 
            self.street_address
        ]
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
        return self.get_full_address().replace("\n", ", ")