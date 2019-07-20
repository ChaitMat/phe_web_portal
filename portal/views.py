from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse

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


    if request.method == "POST":

        form = NewEventForm(request.POST)

        if form.is_valid():

            event = form.save()

            event.save()

            return HttpResponseRedirect(reverse('index') )

    else:

        form = NewEventForm()

    context = {'form': form}

    return render(request, 'portal/event_form.html', context)

          






