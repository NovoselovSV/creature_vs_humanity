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


class HumanSerializer(serializers.ModelSerializer):
    """Serializer for humans."""

    id = serializers.IntegerField()
    health = serializers.IntegerField()
    attack = serializers.IntegerField()


class HumansGroupSerializer(serializers.ModelSerializer):
    """Serializer for group of humans."""

    members = HumanSerializer(many=True)
    signature = serializers.CharField()


class HumanResponseSerializer(serializers.ModelSerializer):
    """Serializer for response about human."""

    id = serializers.IntegerField()
    health = serializers.IntegerField()
    experience = serializers.IntegerField()


class GroupResponseSerializer(serializers.ModelSerializer):
    """Serializer for response about group of humans."""

    members = HumanResponseSerializer(many=True)
    signature = serializers.CharField()
