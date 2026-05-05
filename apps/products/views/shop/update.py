from rest_framework.generics import UpdateAPIView
from apps.products.models import Shop
from apps.products.serializers.request.shop_request import ShopCreateSerializer
from apps.products.schemas.shop.update_schema import shop_update_schema

from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import IsAuthenticated


@extend_schema_view(put=shop_update_schema, patch=shop_update_schema)
class ShopUpdateAPIView(UpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)