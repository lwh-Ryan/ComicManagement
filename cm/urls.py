from django.conf.urls import url, include
from django.contrib.staticfiles import views
from django.contrib import admin
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('management.urls')),
    
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': settings.STATIC_ROOT}, name="static"),
        url(r'^media/(?P<path>.*)$', views.static.serve, {'document_root': settings.MEDIA_ROOT}, name="media")
    ]
