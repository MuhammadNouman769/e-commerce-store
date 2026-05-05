from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.product_response import ProductListSerializer

product_list_schema = extend_schema(
    tags=["Products"],
    summary="Product List",
    responses=ProductListSerializer(many=True),
    description="List all products with main image and price"
)