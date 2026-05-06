from django.urls import path

from apps.products.views.shop_verification.approve import ApproveShopAPIView
from apps.products.views.shop_verification.reject import RejectShopAPIView
from apps.products.views.shop_verification.list import PendingShopListAPIView

urlpatterns = [
    path("shops/pending/", PendingShopListAPIView.as_view(), name="pending-shops"),
    path("shops/<int:id>/approve/", ApproveShopAPIView.as_view(), name="approve-shop"),
    path("shops/<int:id>/reject/", RejectShopAPIView.as_view(), name="reject-shop"),
]