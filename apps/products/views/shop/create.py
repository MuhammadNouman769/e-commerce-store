from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.serializers.request.shop_request import ShopCreateSerializer
from apps.products.services.shop_service import ShopService
from apps.products.schemas.shop.create_schema import shop_create_schema

from drf_spectacular.utils import extend_schema_view

from rest_framework.permissions import IsAuthenticated
from apps.users.choices.role_choices import UserRoleChoices




@extend_schema_view(post=shop_create_schema)
class ShopCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != UserRoleChoices.SELLER:
            return Response({
                "message": "You are not authorized to create a shop"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ShopCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shop = ShopService.create_shop(request.user, serializer.validated_data)

        return Response({
            "message": "Shop created successfully",
            "id": shop.id
        }, status=status.HTTP_201_CREATED)