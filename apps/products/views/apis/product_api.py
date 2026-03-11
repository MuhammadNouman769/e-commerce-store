""" Views for managing categories and products in the e-commerce application. """
from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ...models import Product
from apps.products.serializer import (RecursiveCategorySerializer,ProductSerializer)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
            queryset = queryset.filter(shop_id=shop_id)
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

