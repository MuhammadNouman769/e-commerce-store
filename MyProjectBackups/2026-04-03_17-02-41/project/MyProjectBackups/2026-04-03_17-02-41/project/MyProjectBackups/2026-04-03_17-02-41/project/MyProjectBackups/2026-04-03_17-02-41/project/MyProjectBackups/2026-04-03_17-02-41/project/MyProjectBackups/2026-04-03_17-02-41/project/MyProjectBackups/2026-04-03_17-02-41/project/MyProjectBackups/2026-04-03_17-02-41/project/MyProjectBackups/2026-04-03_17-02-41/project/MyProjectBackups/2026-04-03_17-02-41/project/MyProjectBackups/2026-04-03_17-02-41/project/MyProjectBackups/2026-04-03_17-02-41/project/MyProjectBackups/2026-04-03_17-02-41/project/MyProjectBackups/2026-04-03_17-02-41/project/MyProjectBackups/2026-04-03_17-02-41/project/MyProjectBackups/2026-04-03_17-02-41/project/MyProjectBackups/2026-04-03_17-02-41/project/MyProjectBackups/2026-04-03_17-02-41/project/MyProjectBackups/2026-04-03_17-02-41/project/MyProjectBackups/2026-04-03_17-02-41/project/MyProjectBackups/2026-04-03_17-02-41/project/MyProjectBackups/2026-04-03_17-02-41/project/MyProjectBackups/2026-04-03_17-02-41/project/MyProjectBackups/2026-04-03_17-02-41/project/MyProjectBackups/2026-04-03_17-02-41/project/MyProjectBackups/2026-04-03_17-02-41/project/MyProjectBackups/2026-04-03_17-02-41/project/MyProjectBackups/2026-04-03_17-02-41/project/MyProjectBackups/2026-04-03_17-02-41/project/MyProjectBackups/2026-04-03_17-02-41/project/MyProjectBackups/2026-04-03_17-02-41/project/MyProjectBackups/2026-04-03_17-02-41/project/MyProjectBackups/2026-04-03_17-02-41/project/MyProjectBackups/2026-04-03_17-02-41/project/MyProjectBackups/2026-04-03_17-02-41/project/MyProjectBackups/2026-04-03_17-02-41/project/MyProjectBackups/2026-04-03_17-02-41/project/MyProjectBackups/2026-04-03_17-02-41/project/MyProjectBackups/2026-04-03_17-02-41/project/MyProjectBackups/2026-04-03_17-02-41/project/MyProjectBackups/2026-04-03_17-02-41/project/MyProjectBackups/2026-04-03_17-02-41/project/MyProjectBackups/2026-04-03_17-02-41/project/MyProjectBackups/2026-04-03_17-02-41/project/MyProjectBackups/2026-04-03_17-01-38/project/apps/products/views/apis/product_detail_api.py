""" Views for managing categories and products in the e-commerce application. """
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...models import Product
from apps.products.serializer import ProductSerializer
from django.template.context_processors import request



""" ---------------- Product Detail ---------------- """
class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the product to retrieve",
                type=openapi.TYPE_INTEGER
            )
        ]
    )

    def get(self, request, id):
        """ Retrieve product by id (with categories, images, options and variants)""" 
        product = get_object_or_404(Product.objects.select_related("shop").prefetch_related(
            "categories",
            "images",
            "options__values",
            "variants__option1",
            "variants__option2",
            "variants__option3",
        ), id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, id):
        """ Update product completely by id """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def patch(self, request, id):
        """ Partially update product by id """  
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """ Delete product by id """
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)    