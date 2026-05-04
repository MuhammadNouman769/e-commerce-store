from rest_framework.generics import DestroyAPIView
from apps.products.models import Product


class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = "id"