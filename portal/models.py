from django.db import models
from django.urls import reverse

from .choices import EVENT_TYPES


class Event(models.Model):

    #Date on which the event was created
    time_stamp = models.DateField(auto_now_add = True, help_text = 'Date on which event was created.')

    #Name of the event
    event_name = models.CharField(max_length = 100, help_text = 'Enter the name of the event.')

    #Date of the event
    event_date = models.DateField(help_text = 'Date of the event.')

    #Batch size
    batch_size = models.PositiveIntegerField(help_text = 'Enter batch size.')

    event_type = models.CharField(max_length = 1, choices = EVENT_TYPES, default = 't', help_text = 'Type of event(Trek/Camping)')

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])


class Booking(models.Model):

    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name = 'bookings')

    #Timestamp of the booking made
    time_stamp = models.DateTimeField(auto_now_add = True, help_text = 'Date on which booking was registered.')

    #Name of the participant who made the booking
    booked_by = models.CharField(max_length = 100, help_text = 'Name of the person who made the booking.')

    #Number of participants booked
    participants_count = models.PositiveIntegerField(help_text = 'Number of participants.')

    # Mobile number of the participant who booked
    contact_number = models.PositiveIntegerField(help_text = 'Enter mobile number.', null = True, blank = True)

    date_of_payment = models.DateField(help_text = 'Date of payment.')

    mode_of_payment = models.CharField(max_length = 100, help_text = 'Enter mode of payment.')

    def __str__(self):
        return self.booked_by



