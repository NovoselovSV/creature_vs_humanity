from rest_framework import serializers


from .models import Nest
from area.models import Area
from area.serializers import AreaSerializer


class NestWriteSerializer(serializers.ModelSerializer):
    """Nest serializer for write."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())

    class Meta:
        model = Nest
        fields = ('owner', 'name', 'new_creature_birth_process', 'area')
        read_only_fields = ('new_creature_birth_process',)

    def to_representation(self, nest):
        return NestReadSerializer(nest, context=self.context).data


class NestReadSerializer(serializers.ModelSerializer):
    """Nest serializer for read."""

    area = AreaSerializer()

    class Meta:
        model = Nest
        fields = (
            'id',
            'name',
            'new_creature_birth_process',
            'area',
            'is_giving_birth')
