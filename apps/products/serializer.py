from .models import Category
from rest_framework import serializers

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