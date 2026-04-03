"""

================================================================================
            PRODUCTS MODELS - BTR Mall Product Management
================================================================================
Purpose: Product management, Product variant management, Shop management, 
         Category management, Product image management, variant attribute management
Author: Muhammad Nouman
================================================================================
"""

''' ------------------- IMPORT ------------------- '''
import os
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.conf import settings
from apps.accounts.models import User
from .choices import ProductStatus
from apps.utils.models import(
    BaseModel, 
    OrderedModel, 
    SluggedModel, 
    TimeStampedModel
    )

'''
=========================================================================
1. SHOP MODEL - Seller Storefront
   Usage: Represents a seller's shop with branding and verification
   Features: Multiple shops per user, rating, verification
=========================================================================
'''
class Shop(BaseModel, SluggedModel):
    owner = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        null=False, 
        blank=False, 
        related_name="shop",
        )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        )
    handle = models.SlugField(
        max_length=255, 
        unique=True, 
        blank=True
        )
    description = models.TextField(
        blank=True
        )
    logo = models.ImageField(
        upload_to="shop_logos/%Y/%m/", 
        blank=True, 
        null=True
        )
    banner = models.ImageField(
        upload_to="shop_banners/%Y/%m/", 
        blank=True, 
        null=True
        )
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        null=True,
        blank=True,
        )
    is_verified = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        )

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
        if not self.handle:
            self.handle = self.generate_slug()
        super().save(*args, **kwargs)



'''
=========================================================================
2. CATEGORY MODEL - Product Classifications
    Usage: Organize products into hierarchical categories
    Features: Nested categories, visibility control
=========================================================================
'''
class Category(OrderedModel, SluggedModel):
    parent = models.ForeignKey(
        "self", 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="children"
        )
    name = models.CharField(
        max_length=255
        )
    logo = models.ImageField(
        upload_to="categories/%Y/%m/", 
        blank=True, 
        null=True
        )
    is_visible = models.BooleanField(
        default=True
        )

    class Meta:
        ordering = ["position", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def clean(self):
        if self.parent == self:
            raise ValidationError(
                "Category cannot be parent of itself"
                )
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError(
                    "Circular category structure detected"
                    )
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


'''
=========================================================================
3. PRODUCT MODEL - Core Product Information
   Usage: Main product entity with descriptions, categories, and SEO
   Features: Hierarchical categories, SEO fields, analytics tracking
=========================================================================
'''
class Product(BaseModel, SluggedModel):

    title = models.CharField(
        max_length=255
        )
    short_description = models.CharField(
        max_length=500, 
        blank=True
        )
    description_html = models.TextField(
        blank=True
        )
    categories = models.ManyToManyField(
        Category, 
        related_name="products", 
        blank=True
        )
    brand = models.CharField(
        max_length=255, 
        blank=True
        )
    status = models.CharField(
        max_length=20, 
        choices=ProductStatus.choices, 
        default=ProductStatus.DRAFT
        )
    handle = models.SlugField(
        max_length=255,
        unique=True, 
        blank=True
        )

    # SEO
    meta_title = models.CharField(
        max_length=255, 
        blank=True
        )
    meta_description = models.TextField(
        blank=True
        )
    meta_keywords = models.CharField(
        max_length=500, 
        blank=True
        )

    # Analytics
    total_views = models.PositiveIntegerField(
        default=0
        )
    total_sold = models.PositiveIntegerField(
        default=0
        )
    total_reviews = models.PositiveIntegerField(
        default=0
        )
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0
        )

    # Flags
    is_featured = models.BooleanField(
        default=False
        )
    is_best_seller = models.BooleanField(
        default=False
        )
    is_new = models.BooleanField(
        default=False
        )
    is_on_sale = models.BooleanField(
        default=False
        )    
    
    class Meta:

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)            

    def update_rating(self):
        reviews = self.reviews.filter(is_active=True, is_approved=True)
        self.total_reviews = reviews.count()
        self.average_rating = reviews.aggregate(models.Avg("rating"))["rating__avg"] or 0
        self.save(update_fields=["average_rating", "total_reviews"])



'''
=========================================================================
4. PRODUCT IMAGE MODEL - Visual Assets
   Usage: Store multiple images for each product
   Features: Ordering, alt text, automatic cleanup
=========================================================================
'''
class ProductImage(OrderedModel):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="images"
        )
    image = models.ImageField(
        upload_to="products/gallery/%Y/%m/"
        )
    alt_text = models.CharField(
        max_length=255, 
        blank=True
        )

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




'''
=========================================================================
5. PRODUCT VARIANT MODEL - Stock Keeping Units
   Usage: Manage product variations with unique SKUs and barcodes
   Features: Multiple options, pricing, inventory tracking
=========================================================================
'''
class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="variants"
        )
    sku = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        unique=True
        )
    barcode = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        unique=True
        )

    option1 = models.ForeignKey(
        'ProductOptionValue', 
        on_delete=models.CASCADE, 
        related_name="variants_option1", 
        null=True, 
        blank=True
        )
    option2 = models.ForeignKey(
        "ProductOptionValue", 
        on_delete=models.CASCADE, 
        related_name="variants_option2", 
        null=True, 
        blank=True
        )
    option3 = models.ForeignKey(
        "ProductOptionValue", 
        on_delete=models.CASCADE, 
        related_name="variants_option3", 
        null=True, 
        blank=True
        )

    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2
        )
    compare_at_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
        )



    position = models.PositiveSmallIntegerField(
        default=0
        )

    class Meta:
        unique_together = (
            "product",
            "option1", 
            "option2", 
            "option3"
            )
        ordering = ["position"]
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["sku"]),
        ]    

    def __str__(self):
        return f"{self.product.title}- {self.get_variant_name( ) or self.sku or 'Base'}"

    def get_variant_name(self):
        values = []
        for opt in [self.option1, self.option2, self.option3]:
            if opt:
                values.append(opt.value)
        return " / ".join(values) if values else None



'''
=========================================================================
6. VARIANT IMAGE MODEL - Visual Assets
   Usage: Store multiple images for each product variant
   Features: Ordering, alt text, automatic cleanup
=========================================================================
'''
class VariantImage(OrderedModel):
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.CASCADE, 
        related_name="variant_images"
        )
    image = models.ImageField(
        upload_to="variants/gallery/%Y/%m/"
        )
    alt_text = models.CharField(
        max_length=255, 
        blank=True
        )
    is_main = models.BooleanField(
        default=False
        )

    class Meta:
        ordering = ["position"]
        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"
        unique_together = ["variant", "is_main"]

    def save(self, *args, **kwargs):
        if self.is_main:
            VariantImage.objects.filter(
                variant=self.variant, 
                is_main=True
                ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.product.title} - {self.variant.get_variant_name() or 'Base'} - Image {self.position}"




'''
=========================================================================
7. PRODUCT OPTION MODEL - Variant Dimensions
   Usage: Define options like size, color, material for variants
   Features: Hierarchical options, ordering
=========================================================================
'''
class ProductOption(OrderedModel):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name="options"
        )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]
        verbose_name = "Product Option"
        verbose_name_plural = "Product Options"

    def __str__(self):
        return f"{self.product.title} - {self.name}"



'''
=========================================================================
8. PRODUCT OPTION VALUE MODEL - Variant Values
   Usage: Define specific values for each option (e.g., "Red", "XL")
   Features: Linked to options, ordering
=========================================================================
'''
class ProductOptionValue(OrderedModel):
    option = models.ForeignKey(
        ProductOption, 
        on_delete=models.CASCADE, 
        related_name="values"
        )
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]
        verbose_name = "Product Option Value"
        verbose_name_plural = "Product Option Values"

    def __str__(self):
        return f"{self.option.name}: {self.value}"




'''
=========================================================================
9. PRODUCT REVIEW MODEL - User Feedback
   Usage: Store customer reviews and ratings for products
   Features: Rating system, approval workflow, verified purchase tracking
=========================================================================
'''
class ProductReview(OrderedModel, BaseModel):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="reviews"
        )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="reviews"
        )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} Star") for i in range(1,6)]
        )
    title = models.CharField(
        max_length=200
        )
    comment = models.TextField(
        blank=True
        )
    is_verified_purchase = models.BooleanField(
        default=False
        )
    is_approved = models.BooleanField(
        default=False
        )
    helpful_count = models.PositiveIntegerField(
        default=0
        )

    class Meta:
        unique_together = ["product", "user"]
        ordering = ["-created_at"]
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"{self.user} - {self.product.title} - {self.rating}★"

    def mark_helpful(self):
        ProductReview.objects.filter(
            pk=self.pk
            ).update(
                helpful_count=models.F('helpful_count') + 1
                )


'''
=========================================================================
10. PRODUCT REVIEW IMAGE MODEL - Visual Assets
    Usage: Store images uploaded with product reviews
    Features: Linked to reviews, variant images supported
=========================================================================
'''
class ProductReviewImage(BaseModel):
    review = models.ForeignKey(
        ProductReview, 
        on_delete=models.CASCADE, 
        related_name="images"
        )
    variant_image = models.ForeignKey(
        VariantImage, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="review_images"
        )
    alt_text = models.CharField(
        max_length=255, 
        blank=True
        )

    class Meta:
        verbose_name = "Product Review Image"
        verbose_name_plural = "Product Review Images"
        ordering = ["-created_at"]

    def __str__(self):
        variant_info = self.variant_image.variant.get_variant_name() if self.variant_image else "General"
        return f"{self.review.product.title} - {variant_info} Review Image"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)