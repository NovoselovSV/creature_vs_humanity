from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    # path('area/', include('area.urls')),
    # path('beast/', include('beast.urls')),
    # path('nest/', include('nest.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
