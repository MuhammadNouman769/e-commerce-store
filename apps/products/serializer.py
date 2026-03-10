from .models import Category, Product, ProductImages, ProductOption, ProductOptionValue, ProductVariant
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

""" ===================== Recursive Category Serializer ===================== """
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


""" ===================== ProductOptionValue Serializer ===================== """
class ProductOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = ['id', 'option', 'value', 'position']

""" ===================== ProductOption Serializer ===================== """
class ProductOptionSerializer(serializers.ModelSerializer):
    values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = ['id', 'product', 'name', 'position', 'values']


""" ===================== ProductVariant Serializer ===================== """
class ProductVariantSerializer(serializers.ModelSerializer):
    option1 = ProductOptionSerializer(read_only=True)
    option2 = ProductOptionSerializer(read_only=True)
    option3 = ProductOptionSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'barcode', 'price', 'compare_at_price', 'weight', 'option1', 'option2', 'option3', 'position',]

""" ===================== ProductImage Serializer ===================== """
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'product', 'images', 'alt_text', 'position']



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
            "images",

       ]
        read_only_fields = ["handle", "created_at", "updated_at"]
    def get_category_names(self, obj):
        return [cat.name for cat in obj.categories.all()]
