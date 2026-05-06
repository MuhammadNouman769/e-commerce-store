from rest_framework import serializers
from apps.products.models.category import Category


from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):

    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    @extend_schema_field(str)
    def get_full_path(self, obj):
        return obj.get_full_path()