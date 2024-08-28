from rest_framework import mixins, permissions, viewsets

from . import serializers
from .models import Nest


class NestViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """ViewSet for nest."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.NestSerializer

    def get_queryset(self):
        return Nest.objects.filter(owner=self.kwargs['pk'])
