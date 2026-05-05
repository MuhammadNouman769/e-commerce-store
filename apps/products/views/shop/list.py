from rest_framework.generics import ListAPIView

from apps.products.serializers.response.shop_response import ShopListSerializer
from apps.products.selectors.shop_selector import ShopSelector
from apps.products.schemas.shop.list_schema import shop_list_schema

from drf_spectacular.utils import extend_schema_view


@extend_schema_view(get=shop_list_schema)
class ShopListAPIView(ListAPIView):
    serializer_class = ShopListSerializer

    def get_queryset(self):
        return ShopSelector.list_shops()