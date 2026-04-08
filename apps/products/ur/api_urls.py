from django.urls import path
from apps.products.views.apis.category_api import (
    CategoryListAPIView,
    CategoryDetailAPIView
)
from apps.products.views.apis.product_api import ProductListAPIView
from apps.products.views.apis.product_detail_api import ProductDetailAPIView

urlpatterns = [
    # # ===================== Categories =====================
    # path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    # path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
   

    # # ===================== Products =====================
    # path('products/', ProductListAPIView.as_view(), name='product-list'),
    # path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
]