"""=============== Imports ==============="""
from django.urls import path
from . import views

"""=============== URL Patterns ==============="""
urlpatterns = [
    # Product List with filters
    path('', views.products_list, name='product_list'),

    # Product Detail page
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
