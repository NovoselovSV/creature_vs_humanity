from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

app_name = 'core'

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
