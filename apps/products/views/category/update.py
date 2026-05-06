from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.models import Category
from apps.products.serializers.request.category_request import CategoryCreateUpdateSerializer
from apps.products.serializers.response.category_response import CategorySerializer
from apps.products.services.category_service import CategoryService
from apps.products.schemas.category.update_schema import category_update_schema


class CategoryUpdateAPIView(APIView):

    @category_update_schema
    def put(self, request, pk):
        category = Category.objects.get(pk=pk)

        serializer = CategoryCreateUpdateSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update(category, serializer.validated_data)

        return Response(CategorySerializer(category).data)