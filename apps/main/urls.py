from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/category/', views.category, name='category'),
    # path('contact/', views.contact, name='contact'),
    path('shop/confirm/', views.confirm, name='confirm'),
    path('shop/product-detail/', views.product_detail, name='product_detail'),
    path('shop/cart/', views.cart, name='cart'),
    path('shop/checkout/', views.checkout, name='checkout'),
    path('blog/blog/', views.blog, name='blog'),
    path('blog/single-blog/', views.single_blog, name='single_blog'),
    # path('login/', views.login, name='login'),

]
