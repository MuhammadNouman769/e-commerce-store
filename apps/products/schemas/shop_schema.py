from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from ..serializers.shop_serializer import ShopCreateSerializer


create_shop_schema = extend_schema(
    summary="Create Shop",
    description=(
        "Create a shop for seller.\n\n"
        "🔹 Only sellers can create shop\n"
        "🔹 One user = one shop\n"
        "🔹 Shop will be in pending status until admin approval\n\n"
        "Use Case:\n"
        "- Seller onboarding\n"
        "- First time shop setup"
    ),

    request=ShopCreateSerializer,

    examples=[
        OpenApiExample(
            "Create Shop Example",
            value={
                "name": "My Store",
                "description": "Best store in town",
                "cnic_number": "1234567890123"
            },
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(
            description="Shop created successfully",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Shop created successfully"},
                    "shop_id": {"type": "integer", "example": 1},
                    "status": {"type": "string", "example": "pending"}
                }
            }
        ),
        400: OpenApiResponse(
            description="Validation or business error",
            response={
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "User already has a shop"}
                }
            }
        )
    },

    tags=["Seller / Shop"]
)