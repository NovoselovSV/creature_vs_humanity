from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):
    """User serializer for reading."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserWriteSerializer(UserCreateSerializer):
    """User serializer for writing."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
