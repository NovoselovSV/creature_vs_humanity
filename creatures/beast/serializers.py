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


class BeastBirthSerializer(serializers.ModelSerializer):
    """Beast birth serializer"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Beast
        fields = (
            'owner',
            'name',
            'description')

    def to_representation(self, beast):
        return BeastSerializer(beast).data


class BeastLevelUpAbilitySerializer(serializers.Serializer):
    """Serializer to validate ability name"""

    ability_name = serializers.ChoiceField(
        list(settings.LVL_UP_ABILITY_NAME_VALUE.keys()))
