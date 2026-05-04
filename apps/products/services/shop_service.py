from apps.products.models import Shop


class ShopService:

    @staticmethod
    def create_shop(validated_data):
        return Shop.objects.create(**validated_data)

    @staticmethod
    def update_shop(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


        