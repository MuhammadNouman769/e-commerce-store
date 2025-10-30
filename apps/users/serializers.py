
""" ========== Imports =========== """

from rest_framework import serializers
from .models import User

""" ========== Serializer =========== """

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'is_verified',
            'is_active',
            'date_joined',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_active', 'date_joined', 'created_at', 'updated_at']
