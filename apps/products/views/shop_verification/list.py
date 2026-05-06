from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.products.selectors.shop_verification_selector import ShopVerificationSelector
from apps.products.serializers.response.shop_verification_response import ShopActionResponseSerializer
from apps.products.schemas.shop_verification.list_schema import pending_shop_list_schema


class PendingShopListAPIView(ListAPIView):
    serializer_class = ShopActionResponseSerializer
    permission_classes = [IsAdminUser]

    @pending_shop_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return ShopVerificationSelector.pending_shops()