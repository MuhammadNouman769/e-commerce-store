from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.models import Shop
from apps.products.services.shop_verification_service import ShopVerificationService


class ApproveShopAPIView(APIView):

    def post(self, request, id):
        shop = Shop.objects.get(id=id)

        ShopVerificationService.approve_shop(shop, request.user)

        return Response({
            "message": "Shop approved successfully",
            "shop_id": shop.id
        })