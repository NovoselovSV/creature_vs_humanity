from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """Area serializer."""

    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'description',
            'attacker_attack_impact',
            'attacker_defense_impact',
            'defender_attack_impact',
            'defender_defense_impact'
        )
