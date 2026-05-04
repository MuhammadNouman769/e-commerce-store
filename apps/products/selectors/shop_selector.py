from apps.products.models import Shop


class ShopSelector:

    @staticmethod
    def list_shops():
        return Shop.objects.select_related("owner")