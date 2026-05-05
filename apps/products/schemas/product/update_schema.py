from drf_spectacular.utils import extend_schema
from apps.products.serializers.request.product_request import ProductCreateSerializer

product_update_schema = extend_schema(
    tags=["Products"],
    summary="Update Product",
    request=ProductCreateSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Product updated successfully"}
            }
        }
    }
)