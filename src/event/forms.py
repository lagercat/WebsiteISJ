'''
Created on Jan 10, 2017

@author: roadd
'''
from django.forms import SplitDateTimeWidget
from event.models import Event
from django import forms


class EventCreationFormAdmin(forms.ModelForm):
    time = forms.SplitDateTimeField()

    class Meta:
        model = Event
        fields = ('title', 'description', 'image', 'location')

    def save(self, commit=True):
        event = super(EventCreationFormAdmin, self).save(commit=False)
        event.author = self.current_user
        event.time = self.cleaned_data['time']
        if commit:
            event.save()
        return event
