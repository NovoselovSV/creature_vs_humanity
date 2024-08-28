from rest_framework import mixins, permissions, viewsets

from . import serializers
from .models import Beast


class BeastViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """ViewSet for beast."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.BeastSerializer

    def get_queryset(self):
        return Beast.objects.filter(owner=self.kwargs['pk'])
