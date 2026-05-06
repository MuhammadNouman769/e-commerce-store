from rest_framework import serializers


class ShopCoreResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField(source="shop_status")
    is_verified = serializers.BooleanField()
    



class ShopListResponseSerializer(ShopCoreResponseSerializer):
    owner_email = serializers.EmailField(source="owner.email")
    created_at = serializers.DateTimeField()
    
        

class ShopActionResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    shop = ShopCoreResponseSerializer()    