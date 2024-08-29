from django.conf import settings
from django.core.cache import cache
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from . import serializers
from .models import Nest
from beast.serializers import BeastBirthSerializer
from core.exceptions import BusyException, NotEnoughException


class NestViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for nest."""

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Nest.objects.filter(
            owner=self.request.user).select_related(
            'owner', 'area')

    def get_serializer_class(self):
        if self.action in {'list', 'retrieve'}:
            return serializers.NestReadSerializer
        return serializers.NestWriteSerializer

    @action(methods=('post',), detail=True)
    def birth(self, request, pk):
        nest = get_object_or_404(Nest.objects.all(), pk=pk, owner=request.user)
        if nest.is_giving_birth:
            raise BusyException('Nest is busy')
        if nest.new_creature_birth_process < settings.BIRTH_PROCESS_TO_APPEAR:
            raise NotEnoughException('Not enough birth process')
        new_creature_serializer = BeastBirthSerializer(
            data=request.data, context={'request': request})
        new_creature_serializer.is_valid(raise_exception=True)
        nest.decrease_birth_process(settings.BIRTH_PROCESS_TO_APPEAR)
        new_creature_serializer.save(nest=nest)
        cache.set(
            settings.BIRTH_KEY.format(
                nest=nest),
            True,
            settings.BIRTH_TIME)
        return Response(
            data=new_creature_serializer.data,
            status=status.HTTP_201_CREATED)
