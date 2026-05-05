from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.shop_request import ShopCreateSerializer

shop_create_schema = extend_schema(
    tags=["Shop"],
    summary="Create Shop",
    request=ShopCreateSerializer,
    responses={201: {"type": "object"}},
    examples=[
        OpenApiExample(
            "Create Shop Example",
            value={
                "name": "BTR Store",
                "description": "Best store",
                "cnic_number": "1234567890123"
            }
        )
    ]
)