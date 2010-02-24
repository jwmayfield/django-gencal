from django.conf.urls.defaults import *
from django.views.generic import list_detail
from events.models import Event

event_info = {"queryset": Event.objects.all()}

urlpatterns = patterns('',
    (r'(?P<id>\d+)/$', 'events.views.event_detail'), 
    (r'^$', list_detail.object_list, {"queryset": Event.objects.all()}),
)
