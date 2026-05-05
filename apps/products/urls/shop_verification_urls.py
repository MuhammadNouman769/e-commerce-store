from django.urls import path

from apps.products.views.shop_verification.list import PendingShopListAPIView
from apps.products.views.shop_verification.approve import ApproveShopAPIView
from apps.products.views.shop_verification.reject import RejectShopAPIView


urlpatterns = [
    path("pending/", PendingShopListAPIView.as_view()),
    path("<int:id>/approve/", ApproveShopAPIView.as_view()),
    path("<int:id>/reject/", RejectShopAPIView.as_view()),
]