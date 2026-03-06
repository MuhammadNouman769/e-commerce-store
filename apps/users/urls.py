
from django.urls import path
from . import views

""" ========== URL Patterns =========== """

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

]
