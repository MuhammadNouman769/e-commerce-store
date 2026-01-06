"""=============== Imports ==============="""
from django.urls import path
from .views import ProductListView, ProductDetailView

"""=============== URL Patterns ==============="""
urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]