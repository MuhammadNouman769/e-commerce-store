from django.db import models
from django.utils.text import slugify

from apps.utils.models import SluggedModel
from .shop import Shop
from .category import Category
from apps.common.enums import ProductStatus

""" =================== Product Model ====================== """

class Product(SluggedModel):
    SLUG_FIELD = "title"

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")

    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True)
    description_html = models.TextField(blank=True)

    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    brand = models.CharField(max_length=255, blank=True)

    product_status = models.CharField(
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