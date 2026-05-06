from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.products.serializers.request.category_request import CategoryCreateUpdateSerializer
from apps.products.serializers.response.category_response import CategorySerializer


category_create_schema = extend_schema(
    summary="Create Category",
    request=CategoryCreateUpdateSerializer,
    responses=CategorySerializer,

    examples=[
        OpenApiExample(
            "Create Category",
            value={
                "name": "Electronics",
                "parent": None,
                "is_visible": True
            }
        )
    ],

    tags=["Category"]
)