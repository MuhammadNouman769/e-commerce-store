from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.models import Category
from apps.products.serializers.response.category_response import CategorySerializer
from apps.products.schemas.category.list_schema import category_list_schema


class CategoryListAPIView(APIView):

    @category_list_schema
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)