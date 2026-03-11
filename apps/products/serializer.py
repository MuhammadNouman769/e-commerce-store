from .models import Category, Product, ProductImages, ProductOption, ProductOptionValue, ProductVariant
from rest_framework import serializers

from .scripts.create_test_categories import shop_name


''' ===================== Category Serializer ===================== '''
class CategorySerializer(serializers.ModelSerializer):

    children_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = [
            'id',
            'name', 
            'slug', 
            'parent',  
            'position', 
            'shop',
            'children_count'
        ]
        
# ---------------- Product Option Value Serializer ----------------
class ProductOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = ['id', 'option', 'value', 'position']

# ---------------- Product Option Serializer ----------------
class ProductOptionSerializer(serializers.ModelSerializer):
    values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = ['id', 'product', 'name', 'position', 'values']

# ---------------- Product Variant Serializer ----------------
class ProductVariantSerializer(serializers.ModelSerializer):
    option1 = ProductOptionValueSerializer(read_only=True)
    option2 = ProductOptionValueSerializer(read_only=True)
    option3 = ProductOptionValueSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'barcode', 'price', 'compare_at_price', 'weight', 
                  'option1', 'option2', 'option3', 'position']

# ---------------- Product Image Serializer ----------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'product', 'images', 'alt_text', 'position']

# ---------------- Product Serializer ----------------
class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category_names = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    images = ProductImageSerializer(many=True, read_only=True)
    options = ProductOptionSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'shop', 'shop_name', 'title', 'description_html', 'vendor', 'product_type',
            'status', 'categories', 'category_names', 'published_at', 'created_at', 'updated_at',
            'images', 'options', 'variants'
        ]