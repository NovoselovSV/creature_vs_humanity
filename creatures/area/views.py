from rest_framework import viewsets

from . import serializers
from .models import Area


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for area."""

    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerializer
