from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Product, ProductReview

@receiver(post_save, sender=ProductReview)
def update_product_metrics_on_save(sender, instance, **kwargs):
    """
    auto update metrics of product on product review create/update
    """
    product = instance.product
    reviews = product.reviews.filter(is_active=True, is_approved=True)
    product.total_reviews = reviews.count()
    product.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
    product.save(update_fields=["total_reviews", "average_rating"])


@receiver(post_delete, sender=ProductReview)
def update_product_metrics_on_delete(sender, instance, **kwargs):
    """
    auto update metrics of product on product review delete
    """
    product = instance.product
    reviews = product.reviews.filter(is_active=True, is_approved=True)
    product.total_reviews = reviews.count()
    product.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
    product.save(update_fields=["total_reviews", "average_rating"])
