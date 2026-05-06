from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.category_response import CategorySerializer


category_detail_schema = extend_schema(
    summary="Category Detail",
    responses=CategorySerializer,
    tags=["Category"]
)