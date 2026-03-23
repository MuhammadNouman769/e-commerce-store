
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

""" ========== URL Patterns =========== """

urlpatterns = [
    # Customer routes (defaults)
    path('signup/', views.customer_register, name='register'),
    path('login/', views.customer_login, name='login'),
    # Seller routes
    path('seller/signup/', views.seller_register, name='seller_register'),
    path('seller/login/', views.seller_login, name='seller_login'),
    # Logout ke baad hamesha main home pe redirect
    path('logout/', views.logout_view, name='logout')
]
