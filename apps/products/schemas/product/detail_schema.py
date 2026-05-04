from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.product_response import ProductListSerializer


product_detail_schema = extend_schema(
    responses=ProductListSerializer,
    description="Retrieve single product detail"
)