from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.shop_request import ShopCreateSerializer


shop_create_schema = extend_schema(
    request=ShopCreateSerializer,
    responses={201: {"type": "object"}},
    examples=[
        OpenApiExample(
            "Create Shop",
            value={
                "owner": 1,
                "name": "My Store",
                "description": "Best shop",
                "cnic_number": "1234567890123"
            }
        )
    ]
)