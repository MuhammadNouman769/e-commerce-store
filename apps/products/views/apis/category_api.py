""" Views for managing categories and products in the e-commerce application. """
from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ...models import Category
from apps.products.serializer import (CategorySerializer,
                                      CategoryChildernSerializer,
                                      RecursiveCategorySerializer,
                                      )
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

