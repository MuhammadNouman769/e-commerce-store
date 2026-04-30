from django.urls import path
from ..products.views.product_view import ProductListAPIView, ProductCreateAPIView, ProductDetailAPIView,ProductUpdateAPIView, ProductDeleteAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view()),
    path("products/create/", ProductCreateAPIView.as_view()),
    path("products/<int:pk>/", ProductDetailAPIView.as_view()),
    path("products/<int:pk>/update/", ProductUpdateAPIView.as_view()),
    path("products/<int:pk>/delete/", ProductDeleteAPIView.as_view()),
]