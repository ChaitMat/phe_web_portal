import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import Event, Booking

from portal.forms import NewEventForm, NewBookingForm

        
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


def event_detail_view(request, pk):
    
    event = get_object_or_404(Event, pk=pk)

    form = NewBookingForm()

    if request.method == 'POST'and request.is_ajax():

        form = NewBookingForm(request.POST)

        if form.is_valid():

            b = form.save(commit=False)

            event.bookings.create(
                            booked_by = b.booked_by,
                            participants_count = b.participants_count,
                            contact_number = b.contact_number,
                            date_of_payment = b.date_of_payment,
                            mode_of_payment = b.mode_of_payment,
                        )

            total_participants = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']

            response_data = {}

            response_data['booked_by'] = b.booked_by
            response_data['participants_count'] = b.participants_count
            response_data['contact_number'] = b.contact_number
            response_data['date_of_payment'] = b.date_of_payment.strftime('%B %-d, %Y')
            response_data['mode_of_payment'] = b.mode_of_payment
            response_data['total_participants'] = total_participants
            
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    bookings = event.bookings.all()

    total_participants = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']

    context={
        'event': event,
        'form' : form,
        'bookings' : bookings,
        'total_participants' : total_participants
        }
    
    return render(request, 'portal/event_detail.html', context)


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


# def add_bookings(request, pk):

#     event = get_object_or_404(Event, pk=pk)

#     if request.method == 'POST':

#         form = NewBookingForm(request.POST)

#         print(form)

#         # if form.is_valid():

#         #     event = form.save()

#         #     event.save()

#         return HttpResponseRedirect(reverse('index') )








