from django import forms
from core.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'summary',
            'description',
            'location'
        ]
