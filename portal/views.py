from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


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

    return render(request, 'portal/event_new_form.html', context)


class EventDetailView(generic.DetailView):

    model = Event


def edit_event_form(request, pk):

    event = get_object_or_404(Event, pk=pk)

    date = event.event_date 

    event.event_date = date.strftime("%d/%m/%Y")

    if request.method == "POST":

        form = NewEventForm(request.POST, instance=event)

        if form.is_valid():

            event = form.save()

            event.save()

            return HttpResponseRedirect(reverse('event-detail', args=(event.pk,)))

    else:

        form = NewEventForm(instance=event)

    context = {
        'form' : form,
        'event' : event
        }

    return render(request, 'portal/event_edit_form.html', context)


def delete_event(request, pk):

    event = get_object_or_404(Event, pk=pk)
    event.delete()

    return HttpResponseRedirect(reverse('index'))





          






