from .models import Category
from rest_framework import serializers


''' ===================== Category Serializer ===================== '''
class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "is_active", "position", "description", "image_url"]
    def get_image_url(self,  obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
