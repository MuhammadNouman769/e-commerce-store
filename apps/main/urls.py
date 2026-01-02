from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('about_us/' ,views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('men/', views.men, name='men'),
    path('products_details/', views.products_details, name='products_details'),
   path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('login/', views.login, name='login'),

]
