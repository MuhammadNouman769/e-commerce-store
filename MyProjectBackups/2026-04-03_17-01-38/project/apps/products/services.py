from django.core.cache import cache

def increase_product_view(product_id):
    key = f"product:{product_id}:views"

    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1)