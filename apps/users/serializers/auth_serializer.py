from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "phone", "password", "role"]

    def validate(self, data):
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")

        if User.objects.filter(phone=data["phone"]).exists():
            raise serializers.ValidationError("Phone already exists")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.account_status = "pending"
        user.save()

        return user