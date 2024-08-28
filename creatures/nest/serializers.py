from rest_framework import serializers

from .models import Nest
from area.serializers import AreaSerializer


class NestSerializer(serializers.ModelSerializer):
    """Nest serializer."""

    area = AreaSerializer()

    class Meta:
        model = Nest
        fields = ('name', 'new_creature_birth_process', 'area')
        read_only_fields = ('new_creature_birth_process',)
