from rest_framework.generics import UpdateAPIView
from apps.products.models import Product
from apps.products.serializers.request.product_request import ProductCreateSerializer


class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    lookup_field = "id"