from django import forms
from django.forms import ModelForm
from portal.models import Event

from .choices import EVENT_TYPES

class NewEventForm(ModelForm):

    class Meta:

        model = Event
        fields = '__all__'

    event_date = forms.DateField(
        widget = forms.TextInput(
                                attrs = {

                                    'class' : 'datepicker',
                                }
                            ),
        input_formats=('%d/%m/%Y', )
        )
