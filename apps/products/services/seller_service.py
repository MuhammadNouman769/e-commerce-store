from ..models.shop import Shop


class SellerService:

    @staticmethod
    def create_shop(user, data):

        # role check
        if user.role != "seller":
            return False, "Only seller can create shop"

        # email verification check
        if not user.email_verified:
            return False, "Verify email first"

        # already has shop?
        if hasattr(user, "shop"):
            return False, "Shop already exists"

        shop = Shop.objects.create(
            owner=user,
            **data
        )

        return True, shop