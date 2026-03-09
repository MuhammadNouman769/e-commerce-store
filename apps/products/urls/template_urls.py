""" =========== apps/products/urls/template_urls.py ============ """

from django.urls import path
from ..views.web.product_views import ProductListView, ProductDetailView
from ..views.web.category_views import CategoryListView, CategoryDetailView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    
]