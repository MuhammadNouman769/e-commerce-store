from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.category_response import CategorySerializer


category_list_schema = extend_schema(
    summary="List Categories",
    responses=CategorySerializer(many=True),
    tags=["Category"]
)