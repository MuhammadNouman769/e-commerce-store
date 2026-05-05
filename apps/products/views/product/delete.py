from rest_framework.generics import DestroyAPIView
from apps.products.models import Product
from apps.products.serializers.response.product_response import ProductListSerializer


class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer