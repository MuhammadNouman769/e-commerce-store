from django.urls import path

from apps.products.views.product.create import ProductCreateAPIView
from apps.products.views.product.list import ProductListAPIView
from apps.products.views.product.detail import ProductDetailAPIView
from apps.products.views.product.update import ProductUpdateAPIView
from apps.products.views.product.delete import ProductDeleteAPIView


urlpatterns = [
    path("create/", ProductCreateAPIView.as_view()),
    path("list/", ProductListAPIView.as_view()),
    path("<int:id>/", ProductDetailAPIView.as_view()),
    path("<int:id>/update/", ProductUpdateAPIView.as_view()),
    path("<int:id>/delete/", ProductDeleteAPIView.as_view()),
]