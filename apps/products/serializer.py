from .models import Category, Product
from rest_framework import serializers

from .scripts.create_test_categories import shop_name

''' ===================== Category Childern Serializer ===================== '''
class CategoryChildernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


''' ===================== Category Serializer ===================== '''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent',  'position', 'children', 'shop']
        read_only_fields = ["slug"]

class RecursiveCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent',  'position', 'children', 'shop']
        read_only_fields = ["slug"]

    def get_children(self, obj):
        if obj.children.exists():
            return RecursiveCategorySerializer(obj.children.all(), many=True).data
        return []


""" ===================== Product Serializer ===================== """
class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source="shop.name", read_only=True)
    category_names = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            "id",
            "shop",
            "shop_name",
            "title",
            "description_html",
            "vendor",
            "product_type",
            "status",
            "categories",
            "category_names",
            "published_at",
            "created_at",
            "updated_at",
       ]
        read_only_fields = ["handle", "created_at", "updated_at"]
    def get_category_names(self, obj):
        return [cat.name for cat in obj.categories.all()]
