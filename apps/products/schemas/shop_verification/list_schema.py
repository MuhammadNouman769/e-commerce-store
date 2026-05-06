from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.shop_verification_response import ShopListResponseSerializer


pending_shop_list_schema = extend_schema(
    summary="Pending Shops List",
    description="Get all shops waiting for admin approval",

    tags=["Shop Verification"],

    responses=ShopListResponseSerializer(many=True)
)