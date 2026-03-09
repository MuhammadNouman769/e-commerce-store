from ..views.apis.category_api import (CategoryListAPIView,
                    CategoryDetailAPIView,
                    CategoryUpdateAPIView,
                    CategoryCreateAPIView,
                    CategoryDeleteAPIView,
                    )
from ..views.apis.product_api import ProductListAPIView, ProductDetailAPIView  
from django.urls import path

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('categories/<int:id>/update/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categories/<int:id>/delete/', CategoryDeleteAPIView.as_view(), name='category-delete'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),

]