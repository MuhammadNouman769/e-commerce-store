from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Shop
from apps.products.serializers.response.shop_response import ShopDetailSerializer

@extend_schema_view(
    delete=extend_schema(
        tags=["Shop"],
        summary="Delete Shop",
        description="Delete shop by id",
    )
)
class ShopDeleteAPIView(DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDetailSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)