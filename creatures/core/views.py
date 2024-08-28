from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action

from . import serializers

User = get_user_model()


class UserViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """ViewSet for user flows."""

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in {'list', 'retrieve', 'me'}:
            return serializers.UserReadSerializer
        return serializers.UserWriteSerializer

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        self.kwargs['pk'] = request.user.id
        return self.retrieve(request)
