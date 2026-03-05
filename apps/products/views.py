""" Views for managing categories and products in the e-commerce application. """
from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Category, Product
from apps.products.serializer import (CategorySerializer,
                                      CategoryChildernSerializer,
                                      RecursiveCategorySerializer,
                                      ProductSerializer)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

''' ---------------- List Categories ---------------- '''
class CategoryListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'shop',
                openapi.IN_QUERY,
                description="Filter categories by shop ID",
                type=openapi.TYPE_INTEGER
            )
        ]
    )

    def get(self, request, format=None):
        shop_id = request.query_params.get("shop")
        queryset = Category.objects.all().select_related("parent").prefetch_related("children")
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
      #  serializer = CategorySerializer(queryset, many=True)
        serializer = RecursiveCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


''' ---------------- Category Detail ---------------- '''
class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the category to retrieve",
                type=openapi.TYPE_INTEGER
            )
        ]
    )

    def get(self, request, id, format=None):
        category = get_object_or_404(Category.objects.prefetch_related("children"), id=id)
        serializer = RecursiveCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


''' ---------------- Create Category ---------------- '''
class CategoryCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: "Bad Request"
        }
    )

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' ---------------- Update Category ---------------- '''
class CategoryUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the category to update",
                type=openapi.TYPE_INTEGER
            )
        ],
        request_body=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )

    def put(self, request, id, format=None):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' ---------------- Delete Category ---------------- '''
class CategoryDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the category to delete",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )

    def delete(self, request, id, format=None):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response({"detail": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)


""" ---------------- List Products ---------------- """
class ProductListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    """List all products or filter by shop ID
       list of products with their associated shop,
       categoriesand vendor to minimize database queries"""
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'shop',
                openapi.IN_QUERY,
                description="Filter products by shop ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'vendor',
                openapi.IN_QUERY,
                description="Filter products by vendor name",
                type=openapi.TYPE_STRING
            )
        ]
    )

    def get(self, request):
        shop_id = request.query_params.get("shop")
        vendor_name = request.query_params.get("vendor")
        queryset = Product.objects.all().select_related("shop").prefetch_related("categories")
        if shop_id:
            quesryset = quesryset.filter(shop_id=shop_id)
        if vendor_name:
            queryset = queryset.filter(vendor__iexact=vendor_name)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ Create a new product """
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" ---------------- Product Detail ---------------- """
class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    """ Retrieve a product by ID """
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
        product = get_object_or_404(Product.objects.select_related("shop").prefetch_related("categories"), id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ Update a product by ID """
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Partial update a product by ID """
    def patch(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Delete a product by ID """
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response({"detail": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
