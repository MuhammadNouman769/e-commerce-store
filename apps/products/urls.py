"""=============== Imports ==============="""
from django.urls import path
from . import views

"""=============== URL Patterns ==============="""
urlpatterns = [
    # Product List with filters
    path('', views.products_list, name='products'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
