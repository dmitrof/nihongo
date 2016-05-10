"""nihongo URL Configuration

"""
from django.conf.urls import url, patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^nihongo_tutor/', include('nihongo_tutor.urls', namespace="nihongo_tutor")),
    url(r'^tutor/', include('tutor.urls', namespace="tutor")),
    url(r'^auth/', include('loginsys.urls', namespace="loginsys")),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('tutor.urls', namespace="tutor")),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
