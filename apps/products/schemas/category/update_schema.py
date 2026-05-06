from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.products.serializers.request.category_request import CategoryCreateUpdateSerializer
from apps.products.serializers.response.category_response import CategorySerializer


category_update_schema = extend_schema(
    summary="Update Category",
    request=CategoryCreateUpdateSerializer,
    responses=CategorySerializer,
    tags=["Category"]
)