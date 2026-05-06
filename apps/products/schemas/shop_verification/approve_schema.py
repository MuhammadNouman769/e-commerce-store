from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.shop_verification_response import ShopActionResponseSerializer


approve_shop_schema = extend_schema(
    summary="Approve Shop",
    description="Admin approves a seller shop after verification",

    tags=["Shop Verification"],

    responses={
        200: ShopActionResponseSerializer
    }
)