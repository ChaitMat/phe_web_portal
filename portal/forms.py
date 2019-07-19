from django import forms
from portal.models import Event

class NewEventForm(forms.Form):

    event_name = forms.CharField(max_length = 100, strip =True, help_text = 'Enter the name of the event.')

    event_date = forms.DateField(help_text = 'Enter date of the event.', widget = forms.SelectDateWidget)

    batch_size = forms.IntegerField(help_text = 'Enter batch size.')

    # event_type = forms.ChoiceField(choices = ['Trek', 'Camping'], help_text = 'Enter batch size.')



