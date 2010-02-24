from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^admin/', include(admin.site.urls)),
    (r'^gencal/', include('gencal.urls')),
    (r'^events/', include('events.urls')),
)
