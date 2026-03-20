from django.urls import path
from . import views
from apps.order_fulfillment.views import checkout as checkout_view, confirm as confirm_view

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/category/', views.category, name='category'),
    path('contact-us/', views.contact, name='contact_us'),
    path('shop/confirm/', confirm_view, name='confirm'),
    path('shop/product-detail/', views.product_detail, name='product_detail'),
    path('shop/checkout/', checkout_view, name='checkout'),
    path('blog/blog/', views.blog, name='blog'),
    path('blog/single-blog/', views.single_blog, name='single_blog'),
    path('users/login/', views.login, name='login'),
    path('users/tracking/', views.tracking, name='tracking'),
    path('users/elements/', views.element, name='element'),

]
