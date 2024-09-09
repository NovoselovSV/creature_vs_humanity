import hashlib

from django.conf import settings
from rest_framework import serializers

from .models import Beast
from creatures.celery import app
from nest.serializers import NestReadSerializer


class BeastSerializer(serializers.ModelSerializer):
    """Beast serializer."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nest = NestReadSerializer()

    class Meta:
        model = Beast
        fields = (
            'id',
            'owner',
            'name',
            'description',
            'health',
            'attack',
            'defense',
            'experience',
            'nest',
            'in_nest')
        read_only_fields = (
            'id',
            'health',
            'attack',
            'defense',
            'experience',
            'nest',
            'in_nest')


class BeastWithoutNotOwnerFKsSerializer(serializers.ModelSerializer):
    """Full beast instanse without not owner FKs."""

    class Meta:
        model = Beast
        exclude = ('nest',)


class BeastBirthSerializer(serializers.ModelSerializer):
    """Beast birth serializer."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Beast
        fields = (
            'owner',
            'name',
            'description')

    def to_representation(self, beast):
        return BeastWithoutNotOwnerFKsSerializer(beast).data


class BeastLevelUpAbilitySerializer(serializers.Serializer):
    """Serializer to validate ability name."""

    ability_name = serializers.ChoiceField(
        list(settings.LVL_UP_ABILITY_NAME_VALUE.keys()))


class BeastAttackSerializer(serializers.ModelSerializer):
    """Serializer to attack."""

    signature = serializers.SerializerMethodField()

    class Meta:
        model = Beast
        fields = (
            'name',
            'health',
            'attack',
            'defense',
            'signature')

    def get_signature(self, beast):
        hashed_beast_parametrs = hashlib.sha256()
        hashed_beast_parametrs.update(bytes(str(beast.name), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(beast.health), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(beast.attack), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(beast.defense), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(settings.BEAST_SALT), encoding='utf-8'))
        return hashed_beast_parametrs.hexdigest()


class AttackResponseSerializer(serializers.Serializer):
    """Serializer to attack response."""

    signature = serializers.CharField(write_only=True)
    health = serializers.IntegerField()
    experience = serializers.IntegerField()

    def validate(self, data):
        hashed_beast_parametrs = hashlib.sha256()
        hashed_beast_parametrs.update(
            bytes(str(data.get('health', 0)), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(data.get('experience', 0)), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(settings.BEAST_SALT), encoding='utf-8'))
        if data.get('signature', None) != hashed_beast_parametrs.hexdigest():
            serializers.ValidationError('Signature error')
        return data
