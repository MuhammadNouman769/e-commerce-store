from django.urls import path
from ..views.apis.category_api import (
    CategoryListAPIView,
    CategoryDetailAPIView,
    CategoryCreateAPIView,
    CategoryUpdateAPIView,
    CategoryDeleteAPIView,
)
from ..views.apis.product_api import ProductListAPIView
from ..views.apis.product_detail_api import ProductDetailAPIView  

urlpatterns = [
    # ===================== Categories =====================
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:id>/update/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categories/<int:id>/delete/', CategoryDeleteAPIView.as_view(), name='category-delete'),

    # ===================== Products =====================
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
]