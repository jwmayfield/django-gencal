import datetime

from django.core.exceptions import FieldError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail

from models import GenericCalendar, GenericListCalendar

def calendar(request, calslug, year=None, month=None, day=None):
    today = datetime.datetime.today()
    
    if year is None: year = today.year
    else: year = int(year)
    
    if month is None: month = today.month
    else: month = int(month)
    
    if day is None: day = today.day
    else: day = int(day)

    calendar = GenericCalendar.objects.get(slug=calslug)
    try:
        object_list = calendar.get_objects_for_date(year, month)
    except FieldError:
        object_list = []

    # Populate a dict to be used for the template's context
    d = {'year':year, 'month':month, 'object_list':object_list, 'cal_class':GenericListCalendar }

    return render_to_response('genericcalendar/calendar.html', d, context_instance=RequestContext(request))

def calendar_list(request):
    return list_detail.object_list(
        request,
        queryset = GenericCalendar.objects.all(),
        template_name = 'genericcalendar/list.html',
    )

