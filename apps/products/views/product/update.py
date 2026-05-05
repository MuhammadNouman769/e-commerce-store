from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from apps.products.serializers.request.product_request import ProductCreateSerializer
from apps.products.schemas.product.update_schema import product_update_schema
from apps.common.enums import UserRoleChoices


@extend_schema_view(put=product_update_schema, patch=product_update_schema)
class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == UserRoleChoices.SELLER:
            return Product.objects.filter(shop=self.request.user.shop)
        return Product.objects.none()