from django.conf import settings
from django.core.cache import cache
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import Response

from nest.serializers import NestWriteSerializer

from . import serializers
from .models import Beast
from core.exceptions import BusyException, NotEnoughException


class BeastViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for beast."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.BeastSerializer

    def get_queryset(self):
        return Beast.objects.filter(
            owner=self.request.user).select_related(
            'owner', 'nest', 'nest__area')

    @action(methods=('patch',), detail=True)
    def get_resources_for_nest(self, request, pk):
        beast = self.get_free_beast(request, pk)
        cache.set(
            settings.BEAST_ACTION_KEY.format(beast=beast),
            True,
            settings.BEAST_ACTING_TIME)
        beast.nest.inrease_birth_process(settings.EARNING_BIRTH_PROCESS)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('patch',), detail=True)
    def get_stronger(self, request, pk):
        beast = self.get_free_beast(request, pk)
        cache.set(
            settings.BEAST_ACTION_KEY.format(beast=beast),
            True,
            settings.BEAST_ACTING_TIME)
        beast.increase_experients(settings.EARNING_EXPERIENCE)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('post',), detail=True)
    def attack(self, request, pk):
        raise NotImplementedError

    @action(methods=('post',), detail=True)
    def create_new_nest(self, request, pk):
        beast = self.get_free_beast(request, pk)
        if beast.nest.beasts.count() <= settings.MIN_CREATURE_TO_NEW_NEST:
            raise NotEnoughException(
                f'You need at least {settings.MIN_CREATURE_TO_NEW_NEST} '
                f'creatures in {beast.nest} to create another one')
        cache.set(
            settings.BEAST_ACTION_KEY.format(beast=beast),
            True,
            settings.BEAST_ACTING_TIME)
        new_nest = NestWriteSerializer(
            data=request.data, context={'request': request})
        new_nest.is_valid(raise_exception=True)
        new_nest.save()
        return Response(data=new_nest, status=status.HTTP_201_CREATED)

    @action(methods=('patch',), detail=True)
    def level_up(self, request, pk):
        raise NotImplementedError

    def get_free_beast(self, request, pk):
        beast = get_object_or_404(
            Beast.objects.all(), pk=pk, owner=request.user)
        if not beast.in_nest:
            raise BusyException('Beast is busy')
        return beast
