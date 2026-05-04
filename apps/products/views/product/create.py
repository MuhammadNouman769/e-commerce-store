# views/product/create.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.serializers.request.product_request import ProductCreateSerializer
from apps.products.services.product_service import ProductService

from drf_spectacular.utils import extend_schema_view
from apps.products.schemas.product.create_schema import product_create_schema

@extend_schema_view(post=product_create_schema)
class ProductCreateAPIView(APIView):

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = ProductService.create_product(serializer.validated_data)

        return Response({
            "message": "Product created successfully",
            "id": product.id
        }, status=status.HTTP_201_CREATED)