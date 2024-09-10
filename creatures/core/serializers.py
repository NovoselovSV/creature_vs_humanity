import hashlib

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import MinValueValidator
from rest_framework.generics import ValidationError

from core.shortcuts import get_bytes_from_stringed
from creatures import settings

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


class Human:
    """Support class to map attributes."""

    def __init__(self, id, health, attack, experience=0):
        self.id = id
        self.health = health
        self.attack = attack
        self.experience = experience


class HumanSerializer(serializers.Serializer):
    """Serializer for humans."""

    id = serializers.IntegerField()
    health = serializers.IntegerField(validators=(MinValueValidator(1),))
    attack = serializers.IntegerField()

    def to_representation(self, human):
        return Human(**human)


class HumansGroupSerializer(serializers.Serializer):
    """Serializer for group of humans."""

    members = HumanSerializer(many=True, allow_null=False, allow_empty=False)
    signature = serializers.CharField()

    def validate(self, group_data):
        members = group_data.get('members', [])
        hashed_group_parametrs = hashlib.sha256()
        for member in members:
            hashed_group_parametrs.update(
                get_bytes_from_stringed(member.get('id', 0)))
            hashed_group_parametrs.update(
                get_bytes_from_stringed(member.get('health', 0)))
            hashed_group_parametrs.update(
                get_bytes_from_stringed(member.get('attack', 0)))
        hashed_group_parametrs.update(
            get_bytes_from_stringed(
                settings.HUMANS_SALT))
        if (hashed_group_parametrs.hexdigest()
                != group_data.get('signature', '')):
            raise ValidationError('Signature error')
        return group_data


class HumanResponseSerializer(serializers.Serializer):
    """Serializer for response about human."""

    id = serializers.IntegerField()
    health = serializers.IntegerField()
    experience = serializers.IntegerField()

    def to_internal_value(self, human):
        if isinstance(human, Human):
            human = vars(human)
        return super().to_internal_value(human)


class GroupResponseSerializer(serializers.Serializer):
    """Serializer for response about group of humans."""

    members = HumanResponseSerializer(many=True)
    signature = serializers.SerializerMethodField()

    def get_signature(self, group):
        hashed_group_parametrs = hashlib.sha256()
        for member in group.get('members', []):
            hashed_group_parametrs.update(
                get_bytes_from_stringed(member.get('id', 0)))
            hashed_group_parametrs.update(
                get_bytes_from_stringed(member.get('health', 0)))
            hashed_group_parametrs.update(
                get_bytes_from_stringed(
                    member.get('experience', 0)))
        hashed_group_parametrs.update(
            get_bytes_from_stringed(
                settings.HUMANS_SALT))
        return hashed_group_parametrs.hexdigest()
