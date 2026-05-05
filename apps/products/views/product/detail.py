from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema_view

from apps.products.models import Product
from apps.products.serializers.response.product_response import ProductListSerializer
from apps.products.schemas.product.detail_schema import product_detail_schema


@extend_schema_view(get=product_detail_schema)
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "id"