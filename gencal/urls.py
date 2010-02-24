from django.conf.urls.defaults import *

urlpatterns = patterns('gencal.views',
    url(r'^(?P<calslug>.*)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'calendar', name="genericcalendar-date"),
    url(r'^(?P<calslug>.*)/(?P<year>\d{4})/(?P<month>\d{2})/$', 'calendar', name="genericcalendar-month"),
    url(r'^(?P<calslug>.*)/(?P<year>\d{4})/$', 'calendar', name="genericcalendar-year"),
    url(r'^(?P<calslug>.*)/$', 'calendar', name="genericcalendar-default"),
    url(r'^$', 'calendar_list', name="genericcalendar-list"),
)
