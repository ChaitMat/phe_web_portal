import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from django.template.loader import render_to_string 



from .models import Event, Booking

from portal.forms import NewEventForm, NewBookingForm

# Index page
def eventList(request):
    
    events = Event.objects.all()
    
    for event in events:
        event.total = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']
        event.save()

    context = {'events' : events}
    
    return render(request, 'portal/event_list.html', context=context)

# New event form
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


# View details of an event 
def event_detail_view(request, pk):
    
    event = get_object_or_404(Event, pk=pk)

    form = NewBookingForm()

    bookings = event.bookings.all()

    total_participants = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']

    context={
        'event': event,
        'form' : form,
        'bookings' : bookings,
        'total_participants' : total_participants
        }
    
    return render(request, 'portal/event_detail.html', context)


# Edit an existing event
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


# Delete an existing event
def delete_event(request, pk):

    event = get_object_or_404(Event, pk=pk)
    event.delete()

    return HttpResponseRedirect(reverse('index'))


# Add bookings to an existing event
def add_bookings(request, pk):

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

            update_bookings = event.bookings.all()

            total_participants = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']

            data = dict()

            data['html_bookings_list'] = render_to_string('portal/event_participant_list.html', {'bookings' : update_bookings, 'event' : event})

            data['total_participants'] = total_participants 
            
            return JsonResponse(data)


# Edit bookings from an event
def edit_booking(request, pk, bk):

    event = get_object_or_404(Event, pk=pk)

    booking = get_object_or_404(Booking, pk=bk)

    date = booking.date_of_payment

    booking.date_of_payment = date.strftime("%d/%m/%Y")

    if request.method == "POST":

        form = NewBookingForm(request.POST, instance = booking)

        if form.is_valid():

            booking = form.save()

            booking.save()

            return HttpResponseRedirect(reverse('event-detail', args=(event.pk,)))

    else:

        form = NewBookingForm(instance = booking)

    context = {
        'form' : form,
        'booking' : booking,
        'event' : event
        }

    return render(request, 'portal/booking_edit_form.html', context)
    

# Delete an existing booking
def delete_booking(request, pk, bk):

    event = get_object_or_404(Event, pk=pk)

    booking = get_object_or_404(Booking, pk=bk)

    booking.delete()

    update_bookings = event.bookings.all()

    total_participants = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']

    data = dict()

    data['html_bookings_list'] = render_to_string('portal/event_participant_list.html', {'bookings' : update_bookings, 'event' : event})

    data['total_participants'] = total_participants 

    return JsonResponse(data)

   




