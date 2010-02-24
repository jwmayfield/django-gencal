from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from events.models import Event

def event_detail(request, id):
    event = get_object_or_404(Event, pk=id)
    return render_to_response('events/event_detail.html', {'event':event}, context_instance=RequestContext(request))

