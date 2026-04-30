from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models.review import ProductReview


class ProductReviewAPIView(APIView):

    def post(self, request):
        review = ProductReview.objects.create(
            product_id=request.data["product"],
            user=request.user,
            rating=request.data["rating"],
            title=request.data["title"]
        )
        return Response({"id": review.id})