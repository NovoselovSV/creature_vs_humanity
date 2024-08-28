from rest_framework import serializers

from .models import Beast
from creatures.celery import app
from nest.serializers import NestSerializer


class BeastSerializer(serializers.ModelSerializer):
    """Beast serializer."""

    nest = NestSerializer()
    in_nest = serializers.SerializerMethodField()

    class Meta:
        model = Beast
        fields = (
            'name',
            'description',
            'health',
            'attack',
            'defense',
            'experience',
            'nest',
            'in_nest')
        read_only_fields = (
            'health',
            'attack',
            'defense',
            'experience',
            'nest',
            'in_nest')

    def get_in_nest(self, beast):
        return bool(
            app.AsyncResult(f'Beast_{beast.id}_act').state in {
                'STARTED', 'RETRY'})
