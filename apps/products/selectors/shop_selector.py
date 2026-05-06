from apps.products.models import Shop


class ShopSelector:

    @staticmethod
    def list_shops():
        return Shop.objects.select_related("owner").all()

    @staticmethod
    def get_shop_by_id(shop_id):
        return Shop.objects.select_related("owner").get(id=shop_id)