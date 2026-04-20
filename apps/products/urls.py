from django.urls import path
from .views.seller import CreateShopAPIView

urlpatterns = [
    path("seller/create-shop/", CreateShopAPIView.as_view()),
]