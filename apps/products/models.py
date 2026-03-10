""" =========== Products App Models ==========="""
from contextlib import nullcontext

from django.db import models
from apps.utilities.models import BaseModel
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# from apps.inventory_tracking.models import Warehouse, InventoryItem, InventoryLevel

""" ========== Shop ========== """
class Shop(BaseModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

""" =========== Category =========== """
class Category(BaseModel):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,blank=True
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("shop", "slug")
        ordering = ["position", "name"]
        indexes = [
            models.Index(fields=["shop"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent == self:
            raise ValidationError("Category cannot be parent of itself")
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError("Circular category structure detected")
            parent = parent.parent

    def save(self, *args, **kwargs):
        if not self.slug:
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

        super().save(*args, **kwargs)
    
""" ========== Product =========== """
class Product(BaseModel):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="products"
    )

    class ProductStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=255)
    handle = models.SlugField(max_length=255, blank=True)
    description_html = models.TextField(blank=True)
    vendor = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )
    published_at = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)

    class Meta:
        unique_together = ("shop", "handle")
        indexes = [
            models.Index(fields=["shop", "status"]),
            models.Index(fields=["shop", "handle"]),
        ]

    def save(self, *args, **kwargs):
        """
        Auto-update handle (slug) from title.
        Ensures uniqueness within the same shop.
        """
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        # Exclude self when checking existing handles
        while Product.objects.filter(shop=self.shop, handle=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.handle = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"



""" ============= ProductImages Model ============= """
class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    images = models.ImageField(upload_to="product_images/", null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position"]


""" ======== Product Options and Variants ========== """
class ProductOption(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]

""" =========== Product Option Values =========== """
class ProductOptionValue(BaseModel):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]

""" =========== Product Variant ========== """
class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    option1 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, related_name="variants_option1", null=True, blank=True)
    option2 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, related_name="variants_option2", null=True, blank=True)
    option3 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, related_name="variants_option3", null=True , blank=True)
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("product", "option1", "option2", "option3")
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.product.title} - {self.sku or 'N/A'}"
