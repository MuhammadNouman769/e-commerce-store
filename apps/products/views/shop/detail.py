from rest_framework.generics import RetrieveAPIView
from apps.products.models import Shop
from apps.products.serializers.response.shop_response import ShopDetailSerializer
from apps.products.schemas.shop.detail_schema import shop_detail_schema

from drf_spectacular.utils import extend_schema_view


@extend_schema_view(get=shop_detail_schema)
class ShopDetailAPIView(RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDetailSerializer
    lookup_field = "id"