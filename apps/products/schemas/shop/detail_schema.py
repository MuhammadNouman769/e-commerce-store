from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.shop_response import ShopDetailSerializer


shop_detail_schema = extend_schema(
    responses=ShopDetailSerializer
)