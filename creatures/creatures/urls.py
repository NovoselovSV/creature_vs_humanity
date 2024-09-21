from django.conf import settings
from django.contrib import admin
from django.urls import include, path

api_urls = [
    path('core/', include('core.urls')),
    path('areas/', include('area.urls')),
    path('beasts/', include('beast.urls')),
    path('nests/', include('nest.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    api_urls += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))
]
