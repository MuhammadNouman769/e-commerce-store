from rest_framework.generics import ListAPIView
from apps.products.selectors.shop_verification_selector import ShopVerificationSelector
from apps.products.serializers.response.shop_verification_response import ShopVerificationSerializer


class PendingShopListAPIView(ListAPIView):
    serializer_class = ShopVerificationSerializer

    def get_queryset(self):
        return ShopVerificationSelector.pending_shops()