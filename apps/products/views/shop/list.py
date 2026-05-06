from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.selectors.shop_selector import ShopSelector
from apps.products.serializers.response.shop_response import ShopListSerializer
from apps.products.schemas.shop.list_schema import shop_list_schema


class ShopListAPIView(ListAPIView):
    serializer_class = ShopListSerializer
    permission_classes = [IsAuthenticated]

    @shop_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return ShopSelector.all_shops()