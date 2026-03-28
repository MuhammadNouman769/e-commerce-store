""" =========== Products App Models (Improved) ==========="""
from django.db import models
from django.conf import settings
from apps.utilities.models import BaseModel
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

# ========== Shop ==========
class Shop(BaseModel):
    """Shop/Store model"""
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shop",
        null=True,blank=True,
        verbose_name=_("Owner")
    )
    name = models.CharField(max_length=255, verbose_name=_("Shop Name"))
    domain = models.CharField(max_length=255, unique=True, verbose_name=_("Domain"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    
    # Additional fields
    email = models.EmailField(blank=True, verbose_name=_("Contact Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    logo = models.ImageField(upload_to="shop_logos/", blank=True, null=True)
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")
        indexes = [
            models.Index(fields=["domain"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto cleanup domain"""
        if self.domain:
            self.domain = self.domain.lower().strip()
        super().save(*args, **kwargs)


# ========== Category ==========
class Category(BaseModel):
    """Product Category with hierarchy"""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
        verbose_name=_("Shop")
    )
    name = models.CharField(max_length=255, verbose_name=_("Category Name"))
    slug = models.SlugField(blank=True, verbose_name=_("Slug"))
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name=_("Parent Category")
    )
    position = models.PositiveSmallIntegerField(default=0, verbose_name=_("Position"))
    
    # SEO fields
    description = models.TextField(blank=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)
    is_visible = models.BooleanField(default=True, verbose_name=_("Visible in Store"))

    class Meta:
        unique_together = ("shop", "slug")
        ordering = ["position", "name"]
        indexes = [
            models.Index(fields=["shop"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["shop", "is_visible"]),
        ]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def clean(self):
        """Validate category relationships"""
        if self.parent == self:
            raise ValidationError(_("Category cannot be parent of itself"))
        
        # Check circular reference
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError(_("Circular category structure detected"))
            parent = parent.parent

    def save(self, *args, **kwargs):
        """Auto-generate unique slug"""
        if not self.slug or not self.pk:  # Only generate for new categories
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(
                shop=self.shop,
                slug=slug
            ).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_path(self):
        """Get full category path"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))
    
    @property
    def product_count(self):
        """Get number of active products"""
        return self.products.filter(status=Product.ProductStatus.ACTIVE).count()


# ========== Product ==========
class Product(BaseModel):
    """Product model"""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Shop")
    )

    class ProductStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        ACTIVE = "active", _("Active")
        ARCHIVED = "archived", _("Archived")

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    handle = models.SlugField(max_length=255, blank=True, verbose_name=_("Handle"))
    description_html = models.TextField(blank=True, verbose_name=_("Description"))
    vendor = models.CharField(max_length=255, blank=True, verbose_name=_("Vendor"))
    product_type = models.CharField(max_length=255, blank=True, verbose_name=_("Product Type"))
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT,
        verbose_name=_("Status")
    )
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Published At"))
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True, verbose_name=_("Meta Title"))
    meta_description = models.TextField(blank=True, verbose_name=_("Meta Description"))
    
    # Inventory
    track_inventory = models.BooleanField(default=False, verbose_name=_("Track Inventory"))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_("Stock Quantity"))

    class Meta:
        unique_together = ("shop", "handle")
        indexes = [
            models.Index(fields=["shop", "status"]),
            models.Index(fields=["shop", "handle"]),
            models.Index(fields=["vendor"]),
            models.Index(fields=["status", "published_at"]),
        ]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        """Auto-update handle only when title changes"""
        if not self.handle or not self.pk:  # New product
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Product.objects.filter(shop=self.shop, handle=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.handle = slug
        else:
            # Check if title changed
            original = Product.objects.get(pk=self.pk)
            if original.title != self.title:
                base_slug = slugify(self.title)
                slug = base_slug
                counter = 1

                while Product.objects.filter(shop=self.shop, handle=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                self.handle = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def is_in_stock(self):
        """Check stock availability"""
        if self.track_inventory:
            if self.variants.exists():
                return any(v.is_in_stock for v in self.variants.all())
            return self.stock_quantity > 0
        return True
    
    @property
    def main_image(self):
        """Get first image"""
        return self.images.first()
    
    @property
    def price_range(self):
        """Get price range for variants"""
        if self.variants.exists():
            prices = [v.price for v in self.variants.all()]
            return min(prices), max(prices)
        return None, None


# ========== ProductImages ==========
class ProductImages(BaseModel):
    """Product images"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="images",
        verbose_name=_("Product")
    )
    images = models.ImageField(
        upload_to="product_images/", 
        null=True, 
        blank=True,
        verbose_name=_("Image")
    )
    alt_text = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name=_("Alt Text")
    )
    position = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Position")
    )

    class Meta:
        ordering = ["position"]
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"{self.product.title} - Image {self.position + 1}"
    
    def delete(self, *args, **kwargs):
        """Delete image file when model is deleted"""
        if self.images:
            if os.path.isfile(self.images.path):
                os.remove(self.images.path)
        super().delete(*args, **kwargs)


# ========== Product Options ==========
class ProductOption(BaseModel):
    """Product option (like Size, Color)"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="options",
        verbose_name=_("Product")
    )
    name = models.CharField(max_length=100, verbose_name=_("Option Name"))
    position = models.PositiveSmallIntegerField(verbose_name=_("Position"))

    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]
        verbose_name = _("Product Option")
        verbose_name_plural = _("Product Options")

    def __str__(self):
        return f"{self.product.title} - {self.name}"


# ========== Product Option Values ==========
class ProductOptionValue(BaseModel):
    """Option value (like Small, Red)"""
    option = models.ForeignKey(
        ProductOption, 
        on_delete=models.CASCADE, 
        related_name="values",
        verbose_name=_("Option")
    )
    value = models.CharField(max_length=100, verbose_name=_("Value"))
    position = models.PositiveSmallIntegerField(verbose_name=_("Position"))

    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]
        verbose_name = _("Product Option Value")
        verbose_name_plural = _("Product Option Values")

    def __str__(self):
        return f"{self.option.product.title} - {self.option.name}: {self.value}"


# ========== Product Variant ==========
class ProductVariant(BaseModel):
    """Product variant (like Small Red)"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="variants",
        verbose_name=_("Product")
    )
    barcode = models.CharField(
        max_length=100, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name=_("Barcode")
    )
    sku = models.CharField(
        max_length=100, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name=_("SKU")
    )
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name=_("Price")
    )
    compare_at_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name=_("Compare at Price")
    )
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        null=True, 
        blank=True,
        verbose_name=_("Weight")
    )
    
    # Options
    option1 = models.ForeignKey(
        ProductOptionValue, 
        on_delete=models.CASCADE, 
        related_name="variants_option1", 
        null=True, 
        blank=True,
        verbose_name=_("Option 1")
    )
    option2 = models.ForeignKey(
        ProductOptionValue, 
        on_delete=models.CASCADE, 
        related_name="variants_option2", 
        null=True, 
        blank=True,
        verbose_name=_("Option 2")
    )
    option3 = models.ForeignKey(
        ProductOptionValue, 
        on_delete=models.CASCADE, 
        related_name="variants_option3", 
        null=True, 
        blank=True,
        verbose_name=_("Option 3")
    )
    position = models.PositiveSmallIntegerField(verbose_name=_("Position"))
    
    # Inventory per variant
    track_inventory = models.BooleanField(default=False, verbose_name=_("Track Inventory"))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_("Stock Quantity"))

    class Meta:
        unique_together = ("product", "option1", "option2", "option3")
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["product"]),
            models.Index(fields=["barcode"]),
        ]
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")

    def __str__(self):
        variant_name = self.get_variant_name()
        return f"{self.product.title} - {variant_name or self.sku or 'N/A'}"
    
    def clean(self):
        """Validate variant data"""
        if self.compare_at_price and self.compare_at_price < self.price:
            raise ValidationError({
                'compare_at_price': _("Compare at price cannot be less than regular price")
            })
    
    def save(self, *args, **kwargs):
        """Validate before saving"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        """Check stock availability"""
        if self.track_inventory:
            return self.stock_quantity > 0
        return True
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.compare_at_price and self.compare_at_price > self.price:
            discount = ((self.compare_at_price - self.price) / self.compare_at_price) * 100
            return round(discount, 2)
        return 0
    
    def get_variant_name(self):
        """Generate variant name from options"""
        values = []
        for opt in [self.option1, self.option2, self.option3]:
            if opt:
                values.append(opt.value)
        return " / ".join(values) if values else None
    
    def reduce_stock(self, quantity):
        """Reduce stock when purchased"""
        if self.track_inventory:
            if self.stock_quantity >= quantity:
                self.stock_quantity -= quantity
                self.save()
                return True
            return False
        return True