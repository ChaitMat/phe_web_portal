from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.db.models import Sum

from .models import Event, Booking

from portal.forms import NewEventForm

        
def eventList(request):
    
    events = Event.objects.all()
    
    for event in events:
        event.total = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']
        event.save()

    context = {'events' : events}
    
    return render(request, 'portal/event_list.html', context=context)


def new_event_form(request):

    form = NewEventForm

    context = {

        'form' : form

    }
 
    return render(request, 'portal/new_event.html', context)




