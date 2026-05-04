# services/product_service.py

from apps.products.models import Product


class ProductService:

    @staticmethod
    def create_product(validated_data):
        return Product.objects.create(**validated_data)

    @staticmethod
    def update_product(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance