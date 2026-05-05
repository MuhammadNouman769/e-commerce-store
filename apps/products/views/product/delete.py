from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from apps.products.serializers.response.product_response import ProductListSerializer
from apps.common.enums import UserRoleChoices


@extend_schema_view(
    delete=extend_schema(
        tags=["Products"],
        summary="Delete Product",
        description="Delete product by id",
    )
)
class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == UserRoleChoices.SELLER:
            return Product.objects.filter(shop=self.request.user.shop)
        return Product.objects.none()