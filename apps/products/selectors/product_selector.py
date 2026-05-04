from apps.products.models import Product
from django.db.models import Prefetch


class ProductSelector:

    @staticmethod
    def list_products():
        return Product.objects.prefetch_related(
            "images",
            "variants",
            "categories"
        ).select_related("shop")