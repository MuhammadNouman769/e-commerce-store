from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.models import Category
from apps.products.serializers.response.category_response import CategorySerializer
from apps.products.schemas.category.detail_schema import category_detail_schema


class CategoryDetailAPIView(APIView):

    @category_detail_schema
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        return Response(CategorySerializer(category).data)