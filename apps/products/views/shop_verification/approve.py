from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import status

from apps.products.models import Shop
from apps.products.services.shop_verification_service import ShopVerificationService
from apps.products.schemas.shop_verification.approve_schema import approve_shop_schema
from apps.products.serializers.response.shop_verification_response import ShopApproveResponseSerializer

class ApproveShopAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ShopApproveResponseSerializer

    @approve_shop_schema
    def post(self, request, id):
        shop = get_object_or_404(Shop, id=id)

        shop = ShopVerificationService.approve_shop(shop, request.user)

        return Response(
            {
                "message": "Shop approved successfully",
                "data": {
                    "id": shop.id,
                    "status": shop.status,
                    "is_verified": shop.is_verified,
                    "verified_at": shop.verified_at
                }
            },
            status=status.HTTP_200_OK
        )