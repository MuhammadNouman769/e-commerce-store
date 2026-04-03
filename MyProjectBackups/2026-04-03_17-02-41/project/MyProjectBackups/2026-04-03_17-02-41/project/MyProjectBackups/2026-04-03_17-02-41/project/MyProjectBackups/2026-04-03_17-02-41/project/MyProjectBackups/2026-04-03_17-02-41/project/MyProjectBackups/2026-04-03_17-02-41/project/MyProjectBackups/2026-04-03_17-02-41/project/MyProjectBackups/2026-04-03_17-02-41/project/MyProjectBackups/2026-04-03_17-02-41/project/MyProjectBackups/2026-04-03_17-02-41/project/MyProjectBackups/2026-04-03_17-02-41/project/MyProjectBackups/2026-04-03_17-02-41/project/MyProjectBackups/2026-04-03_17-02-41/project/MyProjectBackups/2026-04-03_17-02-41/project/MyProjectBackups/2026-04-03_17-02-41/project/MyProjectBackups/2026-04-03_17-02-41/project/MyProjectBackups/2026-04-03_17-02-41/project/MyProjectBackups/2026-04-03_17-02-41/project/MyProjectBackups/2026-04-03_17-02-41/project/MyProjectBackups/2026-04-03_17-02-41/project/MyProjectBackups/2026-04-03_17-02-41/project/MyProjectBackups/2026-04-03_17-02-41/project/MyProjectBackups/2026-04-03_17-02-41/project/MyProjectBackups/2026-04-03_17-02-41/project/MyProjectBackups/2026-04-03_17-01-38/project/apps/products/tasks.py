from django.core.cache import cache
from .models import Product

def sync_product_views():
    products = Product.objects.all()

    for product in products:
        key = f"product:{product.id}:views"
        cached_views = cache.get(key)

        if cached_views:
            product.total_views += cached_views
            product.save(update_fields=["total_views"])
            
            cache.delete(key)
        