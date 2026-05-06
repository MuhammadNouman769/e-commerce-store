from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import status

from apps.products.models import Shop
from apps.products.services.shop_verification_service import ShopVerificationService
from apps.products.serializers.request.shop_verification_request import ShopRejectSerializer
from apps.products.schemas.shop_verification.reject_schema import reject_shop_schema
from apps.products.serializers.response.shop_verification_response import ShopActionResponseSerializer


class RejectShopAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ShopActionResponseSerializer

    @reject_shop_schema
    def post(self, request, id):
        serializer = ShopRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shop = get_object_or_404(Shop, id=id)

        shop = ShopVerificationService.reject_shop(
            shop,
            serializer.validated_data["reason"]
        )

        return Response({
            "message": "Shop rejected successfully",
            "shop": {
                "id": shop.id,
                "name": shop.name,
                "status": shop.status,
                "is_verified": shop.is_verified,
                "rejection_reason": shop.rejection_reason
            }
        }, status=status.HTTP_200_OK)