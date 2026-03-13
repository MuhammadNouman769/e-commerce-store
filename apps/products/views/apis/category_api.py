""" Views for managing categories and products in the e-commerce application. """
from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.products.models import Category
from apps.products.serializer import (CategorySerializer)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count

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
        parent_id = request.query_params.get("parent")

        queryset = Category.objects.select_related(
            "parent","shop"
        ).annotate(
            children_count=Count("children")
        )

        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)

        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        else:
            queryset = queryset.filter(parent=None)
                
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



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

    def get(self, request, id):
        """ Retrieve category by id (with parent and children)""" 
        category = get_object_or_404(Category.objects.select_related("parent").prefetch_related("children"), id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)