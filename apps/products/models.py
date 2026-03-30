import os
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL

from apps.utilities.models import BaseModel, OrderedModel, SluggedModel, TimeStampedModel

# ------------------- SHOP MODEL -------------------
class Shop(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop")
    name = models.CharField(max_length=255)
    handle = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="shop_logos/%Y/%m/", blank=True, null=True)
    banner = models.ImageField(upload_to="shop_banners/%Y/%m/", blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
        indexes = [models.Index(fields=["handle"]), models.Index(fields=["owner"])]

    def __str__(self):
        return self.name

    def generate_handle(self):
        base = slugify(self.name)
        slug = base
        counter = 1
        while Shop.objects.filter(handle=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.handle or self._state.adding is False:
            self.handle = self.generate_handle()
        super().save(*args, **kwargs)

# ------------------- CATEGORY MODEL -------------------
class Category(OrderedModel, SluggedModel):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["position", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def clean(self):
        if self.parent == self:
            raise ValidationError("Category cannot be parent of itself")
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError("Circular category structure detected")
            parent = parent.parent

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_path(self):
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))

# ------------------- PRODUCT MODEL -------------------
class Product(BaseModel, SluggedModel):
    class ProductStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"
        OUT_OF_STOCK = "out_of_stock", "Out of Stock"

    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True)
    description_html = models.TextField(blank=True)
    vendor = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.DRAFT)
    handle = models.SlugField(max_length=255, blank=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)

    # Analytics
    total_views = models.PositiveIntegerField(default=0)
    total_sold = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # Flags
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)

    class Meta:
        unique_together = ("handle",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self._state.adding is False:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def update_rating(self):
        reviews = self.reviews.filter(is_active=True, is_approved=True)
        self.total_reviews = reviews.count()
        self.average_rating = reviews.aggregate(models.Avg("rating"))["rating__avg"] or 0
        self.save(update_fields=["average_rating", "total_reviews"])

# ------------------- PRODUCT IMAGE -------------------
class ProductImage(OrderedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/%Y/%m/")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["position"]
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.title} - Image {self.position + 1}"

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

# ------------------- PRODUCT OPTION -------------------
class ProductOption(OrderedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]
        verbose_name = "Product Option"
        verbose_name_plural = "Product Options"

    def __str__(self):
        return f"{self.product.title} - {self.name}"

# ------------------- PRODUCT OPTION VALUE -------------------
class ProductOptionValue(OrderedModel):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]
        verbose_name = "Product Option Value"
        verbose_name_plural = "Product Option Values"

    def __str__(self):
        return f"{self.option.name}: {self.value}"

# ------------------- PRODUCT VARIANT -------------------
class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=100, null=True, blank=True, unique=True)
    barcode = models.CharField(max_length=100, null=True, blank=True, unique=True)

    option1 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, related_name="variants_option1", null=True, blank=True)
    option2 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, related_name="variants_option2", null=True, blank=True)
    option3 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, related_name="variants_option3", null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    track_inventory = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)

    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("product", "option1", "option2", "option3")
        ordering = ["position"]
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return f"{self.product.title} - {self.get_variant_name() or self.sku or 'Base'}"

    def get_variant_name(self):
        values = [opt.value for opt in [self.option1, self.option2, self.option3] if opt]
        return " / ".join(values) if values else None

# ------------------- VARIANT IMAGE -------------------
class VariantImage(OrderedModel):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_images")
    image = models.ImageField(upload_to="variants/gallery/%Y/%m/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]
        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"
        unique_together = ["variant", "is_main"]

    def save(self, *args, **kwargs):
        if self.is_main:
            VariantImage.objects.filter(variant=self.variant, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.product.title} - {self.variant.get_variant_name() or 'Base'} - Image {self.position}"

# ------------------- PRODUCT REVIEW -------------------
class ProductReview(OrderedModel, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Star") for i in range(1,6)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["product", "user"]
        ordering = ["-created_at"]
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"{self.user} - {self.product.title} - {self.rating}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def mark_helpful(self):
        self.helpful_count = models.F('helpful_count') + 1
        self.save(update_fields=['helpful_count'])

# ------------------- PRODUCT REVIEW IMAGE -------------------
class ProductReviewImage(BaseModel):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name="images")
    variant_image = models.ForeignKey(VariantImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="review_images")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Product Review Image"
        verbose_name_plural = "Product Review Images"
        ordering = ["-created_at"]

    def __str__(self):
        variant_info = self.variant_image.variant.get_variant_name() if self.variant_image else "General"
        return f"{self.review.product.title} - {variant_info} Review Image"

    def delete(self, *args, **kwargs):
        if self.variant_image and hasattr(self.variant_image.image, 'path'):
            if os.path.isfile(self.variant_image.image.path):
                os.remove(self.variant_image.image.path)
        super().delete(*args, **kwargs)