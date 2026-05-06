from django.core.exceptions import ValidationError
from apps.products.models import Product
from apps.users.choices.role_choices import UserRoleChoices
from apps.products.choices.shop_status_choices import ShopStatusChoices


class ProductService:

    @staticmethod
    def validate_seller(user):
        if user.role != UserRoleChoices.SELLER:
            raise ValidationError("Only sellers can create products")

        if not hasattr(user, "shop"):
            raise ValidationError("Shop not found")

        if user.shop.status != ShopStatusChoices.APPROVED:
            raise ValidationError("Shop not approved")

        return user.shop

    @staticmethod
    def create(user, validated_data):
        shop = ProductService.validate_seller(user)

        return Product.objects.create(
            shop=shop,
            **validated_data
        )