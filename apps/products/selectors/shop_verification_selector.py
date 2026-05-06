from django.shortcuts import get_object_or_404

from apps.products.models import Shop
from apps.products.choices.shop_status_choices import ShopStatusChoices


class ShopVerificationSelector:

    # =========================
    # BASE QUERY (CORE REUSE)
    # =========================
    @staticmethod
    def base_queryset():
        return Shop.objects.select_related("owner")


    # =========================
    # LIST QUERIES
    # =========================
    @staticmethod
    def pending_shops():
        return ShopVerificationSelector.base_queryset().filter(
            status=ShopStatusChoices.PENDING
        )

    @staticmethod
    def under_review_shops():
        return ShopVerificationSelector.base_queryset().filter(
            status=ShopStatusChoices.UNDER_REVIEW
        )

    @staticmethod
    def approved_shops():
        return ShopVerificationSelector.base_queryset().filter(
            status=ShopStatusChoices.APPROVED
        )

    @staticmethod
    def rejected_shops():
        return ShopVerificationSelector.base_queryset().filter(
            status=ShopStatusChoices.REJECTED
        )


    # =========================
    # GENERIC FILTER (BEST PRACTICE )
    # =========================
    @staticmethod
    def filter_by_status(status=None):
        queryset = ShopVerificationSelector.base_queryset()

        if status:
            return queryset.filter(status=status)

        return queryset


    # =========================
    # SINGLE OBJECT
    # =========================
    @staticmethod
    def get_shop(shop_id):
        return get_object_or_404(
            ShopVerificationSelector.base_queryset(),
            id=shop_id
        )