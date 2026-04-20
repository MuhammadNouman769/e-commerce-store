from django.db import models
from django.utils.text import slugify

from apps.utils.models import SluggedModel
from .shop import Shop
from .category import Category
from ..choices.product_status_choices import ProductStatus
from ..choices.product_status_choices import ProductStatus
"""
=========================================================================
4. PRODUCT MODEL IMPLEMENTATION
   Usage: Represents a product with different options and pricing
   Features:
        - Shop (ForeignKey to Shop model) - the shop that the product belongs to
        - Title (CharField) - the title of the product
        - Short description (CharField) - the short description of the product
        - Description (TextField) - the description of the product
        - Categories (ManyToManyField to Category model) - the categories that the product belongs to
        - Brand (CharField) - the brand of the product
        - Status (CharField) - the status of the product
        - Handle (SlugField) - the handle of the product
        - Meta title (CharField) - the meta title of the product
        - Meta description (TextField) - the meta description of the product
        - Meta keywords (CharField) - the meta keywords of the product
        - Total views (PositiveIntegerField) - the total views of the product
        - Total sold (PositiveIntegerField) - the total sold of the product
        - Total reviews (PositiveIntegerField) - the total reviews of the product
        - Average rating (DecimalField) - the average rating of the product
        - Is featured (BooleanField) - whether the product is featured
        - Is best seller (BooleanField) - whether the product is a best seller
        - Is new (BooleanField) - whether the product is new
        - Is on sale (BooleanField) - whether the product is on sale
=========================================================================
"""

class Product(SluggedModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")

    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True)
    description_html = models.TextField(blank=True)

    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    brand = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )

    handle = models.SlugField(max_length=255, unique=True, blank=True)

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)

    total_views = models.PositiveIntegerField(default=0)
    total_sold = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)

    def generate_handle(self):
        base = slugify(self.title) or "product"
        handle = base
        counter = 1

        while Product.objects.filter(handle=handle).exclude(pk=self.pk).exists():
            handle = f"{base}-{counter}"
            counter += 1
        return handle

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = self.generate_handle()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title