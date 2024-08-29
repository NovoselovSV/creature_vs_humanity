from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import BeastViewSet

app_name = 'beast'

router = SimpleRouter()
router.register('', BeastViewSet, basename='beast')

urlpatterns = [
    path('', include(router.urls)),
]
