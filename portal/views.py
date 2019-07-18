from django.shortcuts import render
from django.views import generic
from django.db.models import Sum

from .models import Event, Booking

        
def eventList(request):
    
    events = Event.objects.all()
    
    for event in events:
        event.total = event.bookings.all().aggregate(Sum('participants_count'))['participants_count__sum']
        event.save()

    context = {'events' : events}
    
    return render(request, 'portal/event_list.html', context=context)