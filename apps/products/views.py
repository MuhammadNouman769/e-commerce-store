from .models import Category
from .serializer import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


''' ===================== Category List View ===================== '''
class CategoryListView(APIView):
    @swagger_auto_schema(
        operation_summary="List all categories",
        operation_description="Returns a list of all product categories"
                              ". Each category includes its name, slug, parent category (if any),"
                              " active status, position, description, and image URL.",
        responses={
            200: openapi.Response(
                description="A list of categories",
                schema=CategorySerializer(many=True)
            )
        }
    )
    def get(self, request):
        """
        Returns all categories as a list.
        Empty list is returned if no categories exist.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


''' ===================== Category Detail View ===================== '''
class CategoryDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve a category by ID",
        operation_description="Returns a single category based on its primary key (id)."
                              " If the category does not exist, a 404 error is returned.",
        responses={
            200: openapi.Response(
                description="A single category",
                schema=CategorySerializer()
            ),
            404: "Category not found"
        }
    )
    def get(self, request, pk):
        """
        Returns a single category by primary key (id).
        Returns 404 if the category does not exist.
        """
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)