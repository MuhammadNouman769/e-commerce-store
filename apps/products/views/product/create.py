# views/product/create.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.serializers.request.product_request import ProductCreateSerializer
from apps.products.services.product_service import ProductService

from drf_spectacular.utils import extend_schema_view
from apps.products.schemas.product.create_schema import product_create_schema
from rest_framework.permissions import IsAuthenticated
from apps.common.enums import UserRoleChoices

@extend_schema_view(post=product_create_schema)
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != UserRoleChoices.SELLER:
            return Response({
                "message": "You are not authorized to create a product"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Ensure the product is created for the user's shop
        validated_data = serializer.validated_data
        validated_data['shop'] = request.user.shop  # Assuming user has a shop field

        product = ProductService.create_product(validated_data)

        return Response({
            "message": "Product created successfully",
            "id": product.id
        }, status=status.HTTP_201_CREATED)