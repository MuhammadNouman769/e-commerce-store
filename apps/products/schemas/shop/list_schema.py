from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.shop_response import ShopListSerializer

shop_list_schema = extend_schema(
    tags=["Shop"],
    summary="Shop List",
    responses=ShopListSerializer(many=True)
)