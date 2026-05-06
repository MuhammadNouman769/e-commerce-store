from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "phone", "password", "confirm_password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Email already exists")

        if User.objects.filter(phone=attrs["phone"]).exists():
            raise serializers.ValidationError("Phone already exists")

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        user.email_verified = False
        user.account_status = "pending"

        user.save()
        return user