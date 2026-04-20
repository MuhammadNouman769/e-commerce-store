from django.db import models
from apps.utils.models import OrderedModel, BaseModel

from .product import Product
from .variant import ProductVariant
from .product_image import ProductImage, VariantImage
from apps.users.models.users import User


"""
=========================================================================
3. PRODUCT REVIEW MODEL IMPLEMENTATION
   Usage: Represents a review of a product by a user
   Features:
        - Product (ForeignKey to Product model) - the product that the review belongs to
        - User (ForeignKey to User model) - the user who wrote the review
        - Rating (PositiveSmallIntegerField) - the rating of the review
        - Title (CharField) - the title of the review
        - Comment (TextField) - the comment of the review
        - Is verified purchase (BooleanField) - whether the purchase is verified
        - Is approved (BooleanField) - whether the review is approved
        - Helpful count (PositiveIntegerField) - the helpful count of the review
=========================================================================
"""

class ProductReview(OrderedModel, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")

    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    title = models.CharField(max_length=200)
    comment = models.TextField(blank=True)

    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["product", "user"]

    def __str__(self):
        return f"{self.user} - {self.product.title} - {self.rating}★"


class ProductReviewImage(BaseModel):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name="images")
    variant_image = models.ForeignKey(VariantImage, on_delete=models.SET_NULL, null=True, blank=True)

    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.review.product.title} Review Image"