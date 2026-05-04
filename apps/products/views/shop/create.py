from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.serializers.request.shop_request import ShopCreateSerializer
from apps.products.services.shop_service import ShopService
from apps.products.schemas.shop.create_schema import shop_create_schema

from drf_spectacular.utils import extend_schema_view


@extend_schema_view(post=shop_create_schema)
class ShopCreateAPIView(APIView):

    def post(self, request):
        serializer = ShopCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shop = ShopService.create_shop(serializer.validated_data)

        return Response({
            "message": "Shop created successfully",
            "id": shop.id
        }, status=status.HTTP_201_CREATED)