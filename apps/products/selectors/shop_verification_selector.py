from apps.products.models import Shop
from apps.products.choices.shop_status_choices import ShopStatusChoices


class ShopVerificationSelector:

    @staticmethod
    def pending_shops():
        return Shop.objects.filter(
            status=ShopStatusChoices.PENDING
        ).select_related("owner")

    @staticmethod
    def get_shop(shop_id):
        return Shop.objects.select_related("owner").get(id=shop_id)