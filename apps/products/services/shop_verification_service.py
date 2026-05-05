from django.utils import timezone
from apps.products.choices.shop_status_choices import ShopStatusChoices


class ShopVerificationService:

    @staticmethod
    def approve_shop(shop, admin_user):
        shop.status = ShopStatusChoices.APPROVED
        shop.is_verified = True
        shop.verified_at = timezone.now()
        shop.rejection_reason = ""
        shop.save(update_fields=[
            "status",
            "is_verified",
            "verified_at",
            "rejection_reason"
        ])
        return shop

    @staticmethod
    def reject_shop(shop, reason):
        shop.status = ShopStatusChoices.REJECTED
        shop.is_verified = False
        shop.rejection_reason = reason
        shop.save(update_fields=[
            "status",
            "is_verified",
            "rejection_reason"
        ])
        return shop

    @staticmethod
    def send_to_review(shop):
        shop.status = ShopStatusChoices.UNDER_REVIEW
        shop.save(update_fields=["status"])
        return shop