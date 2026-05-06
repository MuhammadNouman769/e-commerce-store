from rest_framework import serializers


class ShopRejectSerializer(serializers.Serializer):
    reason = serializers.CharField(
        max_length=500,
        help_text="Reason for rejecting the shop"
    )


class ShopReviewSerializer(serializers.Serializer):
    note = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text="Optional admin review note"
    )