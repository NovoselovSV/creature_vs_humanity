from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import MinValueValidator

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


class GroupAttackSerializer(serializers.Serializer):
    """Serializer for attack on group."""

    id = serializers.IntegerField()


class HumanSerializer(serializers.Serializer):
    """Serializer for humans."""

    id = serializers.IntegerField()
    health = serializers.IntegerField(validators=(MinValueValidator(1),))
    attack = serializers.IntegerField()


class HumansGroupSerializer(serializers.Serializer):
    """Serializer for group of humans."""

    members = HumanSerializer(many=True)
    signature = serializers.CharField()


class HumanResponseSerializer(serializers.Serializer):
    """Serializer for response about human."""

    id = serializers.IntegerField()
    health = serializers.IntegerField()
    experience = serializers.IntegerField()


class GroupResponseSerializer(serializers.Serializer):
    """Serializer for response about group of humans."""

    members = HumanResponseSerializer(many=True)
    signature = serializers.CharField()
