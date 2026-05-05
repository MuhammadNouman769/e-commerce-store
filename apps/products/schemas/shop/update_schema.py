from drf_spectacular.utils import extend_schema
from apps.products.serializers.request.shop_request import ShopCreateSerializer

shop_update_schema = extend_schema(
    tags=["Shop"],
    summary="Update Shop",
    request=ShopCreateSerializer,
    responses={200: {"type": "object"}}
)