from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import NestViewSet

app_name = 'nest'

router = SimpleRouter()
router.register('', NestViewSet, basename='nest')

urlpatterns = [
    path('', include(router.urls)),
]
