from rest_framework import serializers


# =========================
# 1. CORE SHOP DATA
# =========================
class ShopCoreResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField()
    is_verified = serializers.BooleanField()


# =========================
# 2. BASE ACTION RESPONSE
# =========================
class ShopActionResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    shop = ShopCoreResponseSerializer()


# =========================
# 3. APPROVE RESPONSE
# =========================
class ShopApproveResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    shop = ShopCoreResponseSerializer()
    verified_at = serializers.DateTimeField()


# =========================
# 4. REJECT RESPONSE
# =========================
class ShopRejectResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    shop = ShopCoreResponseSerializer()
    rejection_reason = serializers.CharField()


# =========================
# 5. REVIEW RESPONSE
# =========================
class ShopReviewResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    shop = ShopCoreResponseSerializer()
    note = serializers.CharField(required=False, allow_null=True)


# =========================
# 6. LIST RESPONSE (ADMIN PANEL)
# =========================
class ShopListResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    owner_email = serializers.EmailField(source="owner.email")
    status = serializers.CharField()
    is_verified = serializers.BooleanField()
    created_at = serializers.DateTimeField()