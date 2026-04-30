# views/product.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.models.product import Product
from apps.products.serializers import (
    ProductCreateSerializer,
    ProductListSerializer,
    ProductDetailSerializer
)
from apps.products.services.product_service import ProductService


class ProductCreateAPIView(APIView):

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)

        if serializer.is_valid():
            product = ProductService.create_product(serializer)
            return Response({"id": product.id}, status=201)

        return Response(serializer.errors, status=400)


class ProductListAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductUpdateAPIView(APIView):

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data)

        if serializer.is_valid():
            ProductService.update_product(product, serializer)
            return Response({"message": "updated"})

        return Response(serializer.errors, status=400)


class ProductDeleteAPIView(APIView):

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        ProductService.delete_product(product)
        return Response({"message": "deleted"})