

""" ========== Imports =========== """

from django.urls import path
from . import views

""" ========== URL Patterns =========== """

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
]
