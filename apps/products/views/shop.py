from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.shop_serializer import ShopCreateSerializer
from ..services.seller_service import SellerService
from ..schemas.shop_schema import create_shop_schema


class CreateShopAPIView(APIView):

    @create_shop_schema
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