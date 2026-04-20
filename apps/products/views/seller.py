from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.shop_serializer import ShopCreateSerializer
from ..services.seller_service import SellerService


class CreateShopAPIView(APIView):

    def post(self, request):

        serializer = ShopCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        success, result = SellerService.create_shop(
            request.user,
            serializer.validated_data
        )

        if not success:
            return Response({"error": result}, status=400)

        return Response({
            "message": "Shop created successfully",
            "shop_id": result.id,
            "status": result.status
        })