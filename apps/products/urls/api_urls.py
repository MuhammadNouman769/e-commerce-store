from django.urls import path
from ..views.apis.category_api import (
    CategoryListAPIView
   
)
from ..views.apis.product_api import ProductListAPIView
from ..views.apis.product_detail_api import ProductDetailAPIView  

urlpatterns = [
    # ===================== Categories =====================
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
   

    # ===================== Products =====================
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
]