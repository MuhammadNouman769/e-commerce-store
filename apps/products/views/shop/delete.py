from rest_framework.generics import DestroyAPIView
from apps.products.models import Shop
from apps.products.serializers.response.shop_response import ShopDetailSerializer

class ShopDeleteAPIView(DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDetailSerializer   # add this
    lookup_field = "id"