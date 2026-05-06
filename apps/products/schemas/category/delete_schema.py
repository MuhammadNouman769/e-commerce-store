from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.category_response import CategorySerializer

from drf_spectacular.utils import OpenApiResponse

category_delete_schema = extend_schema(
    summary="Delete Category",
    responses=OpenApiResponse(
        response={
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        }
    )
)