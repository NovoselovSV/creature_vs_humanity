from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AreaViewSet

app_name = 'area'

router = SimpleRouter()
router.register('', AreaViewSet, basename='area')

urlpatterns = [
    path('', include(router.urls)),
]
