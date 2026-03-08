from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/category/', views.category, name='category'),
    path('contact-us/', views.contact, name='contact_us'),
    path('shop/confirm/', views.confirm, name='confirm'),
    path('shop/product-detail/', views.product_detail, name='product_detail'),
    path('shop/cart/', views.cart, name='cart'),
    path('shop/checkout/', views.checkout, name='checkout'),
    path('blog/blog/', views.blog, name='blog'),
    path('blog/single-blog/', views.single_blog, name='single_blog'),
    path('users/login/', views.login, name='login'),
    path('users/tracking/', views.tracking, name='tracking'),
    path('users/elements/', views.element, name='element'),

]
