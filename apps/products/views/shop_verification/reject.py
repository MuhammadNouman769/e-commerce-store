from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.models import Shop
from apps.products.serializers.request.shop_verification_request import ShopRejectSerializer
from apps.products.services.shop_verification_service import ShopVerificationService


class RejectShopAPIView(APIView):

    def post(self, request, id):
        serializer = ShopRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shop = Shop.objects.get(id=id)

        ShopVerificationService.reject_shop(
            shop,
            serializer.validated_data["reason"]
        )

        return Response({
            "message": "Shop rejected",
            "shop_id": shop.id
        })