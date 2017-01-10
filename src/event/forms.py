'''
Created on Jan 10, 2017

@author: roadd
'''
from event.models import Event
from django import forms

class EventCreationFormAdmin(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'image', 'time', 'location')

    def save(self, commit=True):
        event = super(EventCreationFormAdmin, self).save(commit=False)
        event.author = self.current_user
        if commit:
            event.save()
        return event