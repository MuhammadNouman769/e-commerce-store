from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.shop_response import ShopListSerializer


shop_list_schema = extend_schema(
    summary="All Shops List",
    description="Get all shops (admin or public listing)",
    responses=ShopListSerializer(many=True),
    tags=["Shop"]
)