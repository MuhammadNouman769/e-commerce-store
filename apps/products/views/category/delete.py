from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.models import Category
from apps.products.services.category_service import CategoryService
from apps.products.schemas.category.delete_schema import category_delete_schema


class CategoryDeleteAPIView(APIView):

    @category_delete_schema
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        CategoryService.delete(category)

        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_200_OK
        )