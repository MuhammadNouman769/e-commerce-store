# schemas/product/create_schema.py

from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.product_request import ProductCreateSerializer


product_create_schema = extend_schema(
    request=ProductCreateSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Product created successfully"},
                "id": {"type": "integer", "example": 1}
            }
        }
    },
    examples=[
        OpenApiExample(
            "Create Product Example",
            value={
                "shop": 1,
                "title": "iPhone 15 Pro",
                "short_description": "Latest iPhone",
                "description_html": "<p>Best phone</p>",
                "categories": [1, 2],
                "brand": "Apple",
                "status": "draft",
                "is_featured": True,
                "is_best_seller": False,
                "is_new": True,
                "is_on_sale": False
            }
        )
    ]
)