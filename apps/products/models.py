''' =============== Imports =============== '''
from django.db import models
from apps.utilities.models import BaseModel
from django.utils.text import slugify
from django.utils.crypto import get_random_string


''' ============== Start Product Model =============== '''
class Product(BaseModel):

    # === Improvement: Product Status Choices Added ===
    class ProductStatus(models.IntegerChoices):
        DRAFT = 1, "Draft"
        ACTIVE = 2, "Active"
        ARCHIVED = 3, "Archived"


    title = models.CharField(max_length=255)

    # === Improvement: Auto Slug Handle ===
    handle = models.SlugField(max_length=255, blank=True)

    description_html = models.TextField(blank=True)

    vendor = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)

    status = models.PositiveSmallIntegerField(
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )

    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("shop", "handle")
        indexes = [
            models.Index(fields=["shop", "status"]),
            # === Improvement: Performance Index Added ===
            models.Index(fields=["shop", "published_at"]),
        ]

    # === Improvement: Auto Generate Unique Handle ===
    def save(self, *args, **kwargs):
        if not self.handle:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(shop=self.shop, handle=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.handle = slug
        super().save(*args, **kwargs)


''' ------------- End Product Model --------------- '''



''' =============== Start ProductOption Model ============== '''
class ProductOption(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options"
    )

    name = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]

''' ------------ End ProductOption Model ------------- '''



''' ============ Start ProductOptionValue Model ============ '''
class ProductOptionValue(BaseModel):
    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]

''' ------------- End ProductOptionValue Model ------------ '''



''' ============= Start ProductVariant Model ============== '''
class ProductVariant(BaseModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="variants"
    )

    # Identity
    barcode = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100)

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Physical properties
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
    )

    # Option combination
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)

    # === Improvement: Removed default=1 to avoid duplicate positions ===
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (
            "product",
            "option1",
            "option2",
            "option3",
        )
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.product.title} - {self.sku}"


''' ------------- End ProductVariant ------------- '''



'''
---------------------------------------
Inventory Item (links variant to stock)
----------------------------------------
'''
class InventoryItem(BaseModel):
    variant = models.OneToOneField(
        ProductVariant,
        related_name='inventory_item',
        on_delete=models.CASCADE
    )

    # === Improvement: Removed Duplicate SKU & Barcode ===
    tracked = models.BooleanField(default=True)
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )



'''
--------------------------------
 Inventory Level (per location)
--------------------------------
'''
class InventoryLevel(BaseModel):
    inventory_item = models.ForeignKey(
        InventoryItem,
        related_name='levels',
        on_delete=models.CASCADE
    )

    location = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE
    )

    available_quantity = models.IntegerField(default=0)
    incoming_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('inventory_item', 'location')



''' ============= Category Model ============== '''
class Category(BaseModel):
    name = models.CharField(max_length=255)

    # === Improvement: Slug Auto Generate with Collision Handling ===
    slug = models.SlugField(unique=True, blank=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    is_active = models.BooleanField(default=True)

    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="category_images/",
        null=True,
        blank=True
    )

    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["position", "name"]
        # === Improvement: Performance Index Added ===
        indexes = [
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return self.name

    # === Improvement: Unique Slug Generator ===
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

''' ------------- End Category ------------- '''