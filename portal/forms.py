import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from portal.models import Event, Booking

from .choices import EVENT_TYPES

class NewEventForm(ModelForm):

    def clean_event_date(self):
        data = self.cleaned_data['event_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Select date from the future'))

        return data

    class Meta:

        model = Event
        fields = '__all__'

    event_date = forms.DateField(
        widget = forms.TextInput(
                                attrs = {

                                    'class' : 'datepicker',
                                }
                            ),
        input_formats=('%d/%m/%Y', ),
        help_text = 'Enter event date.'
        )

class NewBookingForm(ModelForm):

    def clean_event_date(self):
        data = self.cleaned_data['event_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Select date from the future'))

        return data
    
    class Meta:

        model = Booking
        exclude = ['event']

    date_of_payment = forms.DateField(
        widget = forms.TextInput(
                                attrs = {

                                    'class' : 'datepicker',
                                }
                            ),
        input_formats=('%d/%m/%Y', ),
        help_text = 'Enter date of payment.'
        )

    