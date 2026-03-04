from .views import CategoryListAPIView, CategoryDetailAPIView, CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView
from django.urls import path

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('categories/<int:id>/update/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categories/<int:id>/delete/', CategoryDeleteAPIView.as_view(), name='category-delete'),

]