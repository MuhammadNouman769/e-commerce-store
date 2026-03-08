from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/category/', views.category, name='category'),
    # path('contact/', views.contact, name='contact'),
    # path('men/', views.men, name='men'),
    path('products/product_detail/', views.product_detail, name='product_detail'),
    path('products/cart/', views.cart, name='cart'),
    path('products/checkout/', views.checkout, name='checkout'),
    # path('order_complete/', views.order_complete, name='order_complete'),
    # path('wishlist/', views.wishlist, name='wishlist'),
    # path('login/', views.login, name='login'),

]
