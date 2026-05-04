from rest_framework.generics import DestroyAPIView
from apps.products.models import Shop


class ShopDeleteAPIView(DestroyAPIView):
    queryset = Shop.objects.all()
    lookup_field = "id"