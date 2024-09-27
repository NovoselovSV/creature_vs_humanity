from random import choice

from django.conf import settings
from django.core.cache import cache
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import Response

from . import serializers, tasks
from .models import Beast
from area.models import Area
from beast.attack import request_group_attack
from core.exceptions import BusyException, NotEnoughException
from core.fight import fight
from core.serializers import GroupAttackSerializer, HumansGroupSerializer
from nest.serializers import NestWriteSerializer


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
        self.add_task_for_beast(
            beast, tasks.obtain_resources_for_nest, beast.id)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('patch',), detail=True)
    def get_stronger(self, request, pk):
        beast = self.get_free_beast(request, pk)
        self.add_task_for_beast(beast, tasks.obtain_experience, beast.id)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('post',), detail=True)
    def attack(self, request, pk):
        beast = self.get_free_beast(request, pk)
        attacked_group = GroupAttackSerializer(data=request.data)
        attacked_group.is_valid(raise_exception=True)
        return Response(
            data=request_group_attack(
                beast, attacked_group.data.get(
                    'id', 0)), status=status.HTTP_201_CREATED)

    @action(methods=('post',), detail=True)
    def create_new_nest(self, request, pk):
        beast = self.get_free_beast(request, pk)
        if beast.nest.beasts.count() <= settings.MIN_CREATURE_TO_NEW_NEST:
            raise NotEnoughException(
                f'You need at least {settings.MIN_CREATURE_TO_NEW_NEST} '
                f'creatures in {beast.nest} to create another one')
        new_nest = NestWriteSerializer(
            data=request.data, context={'request': request})
        new_nest.is_valid(raise_exception=True)
        self.add_task_for_beast(beast,
                                tasks.create_nest,
                                beast.id,
                                request.user.id,
                                new_nest.data)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=('patch',), detail=True)
    def level_up(self, request, pk):
        beast = self.get_free_beast(request, pk)
        ability_name_serializer = serializers.BeastLevelUpAbilitySerializer(
            data=request.data)
        ability_name_serializer.is_valid(raise_exception=True)
        ability_name = ability_name_serializer.data['ability_name']
        if beast.experience < settings.NEW_LEVEL_EXPERIENTS:
            raise NotEnoughException(
                'This beast must have at least '
                f'{settings.NEW_LEVEL_EXPERIENTS} experience '
                'to level up')
        beast.level_up(ability_name)
        return Response(status=status.HTTP_200_OK)

    @action(url_path='_defense', permission_classes=(permissions.AllowAny,),
            methods=('post',), detail=True)
    def defense(self, request, pk):
        beast = self.get_beast(request, pk)
        group_serializer = HumansGroupSerializer(data=request.data)
        group_serializer.is_valid(raise_exception=True)
        if beast.in_nest:
            raise BusyException('Beast in nest')
        response_serializer = fight(
            beast,
            group_serializer.data['members'],
            choice(tuple(Area.objects.all())))
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED)

    def add_task_for_beast(self, beast, task, *args):
        key = settings.BEAST_ACTION_KEY.format(beast=beast)
        cache.set(
            key,
            str(task.apply_async(
                (*args, key),
                countdown=settings.BEAST_ACTING_TIME)),
            settings.BEAST_ACTING_TIME * settings.BUFFER_MULTIPLY)

    def get_beast(self, request, pk):
        return get_object_or_404(
            self.get_queryset(), pk=pk)

    def get_free_beast(self, request, pk):
        beast = self.get_beast(request, pk)
        if not beast.in_nest:
            raise BusyException('Beast is busy')
        return beast
