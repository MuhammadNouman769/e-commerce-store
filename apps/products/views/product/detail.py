from rest_framework.generics import RetrieveAPIView
from apps.products.models import Product
from apps.products.serializers.response.product_response import ProductListSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "id"