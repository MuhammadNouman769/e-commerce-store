from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models.category import Category
from products.serializers.request.product_request import ProductCreateSerializer
from products.serializers.response.product_response import ProductListSerializer, ProductDetailSerializer

from apps.products.services.product_service import ProductService



class CategoryAPIView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        return Response([{"id": c.id, "name": c.name} for c in categories])

    def post(self, request):
        category = Category.objects.create(name=request.data.get("name"))
        return Response({"id": category.id})