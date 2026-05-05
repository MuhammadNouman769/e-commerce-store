from rest_framework.generics import ListAPIView
from apps.products.serializers.response.product_response import ProductListSerializer
from apps.products.selectors.product_selector import ProductSelector

from drf_spectacular.utils import extend_schema_view
from apps.products.schemas.product.list_schema import product_list_schema


@extend_schema_view(get=product_list_schema)
class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return ProductSelector.list_products()