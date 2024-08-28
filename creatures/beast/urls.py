from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = 'beast'

router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
]
