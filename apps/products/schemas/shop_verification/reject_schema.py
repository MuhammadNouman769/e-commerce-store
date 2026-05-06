from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.shop_verification_request import ShopRejectSerializer
from apps.products.serializers.response.shop_verification_response import ShopRejectResponseSerializer

reject_shop_schema = extend_schema(
    summary="Reject Shop",
    description="Admin rejects a shop with a reason",

    tags=["Shop Verification"],

    request=ShopRejectSerializer,

    examples=[
        OpenApiExample(
            name="Reject Shop Example",
            value={
                "reason": "Invalid CNIC document"
            },
            request_only=True
        )
    ],

    responses={
        200: ShopRejectResponseSerializer
    }
)