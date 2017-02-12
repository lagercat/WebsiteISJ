from django.contrib import admin
from models import Event
from view_permission.admin import AdminViewMixin
from django import forms

from event.forms import EventCreationFormAdmin, EventChangeFormAdmin
# Register your models here.

class EventAdmin(AdminViewMixin):
    add_form = EventCreationFormAdmin
    change_form = EventChangeFormAdmin

    icon = '<i class="material-icons">room</i>'

    list_display = ('name', 'author', 'event_location', 'date', 'slug',)
    readonly_fields = ['author']
    
    search_fields = ('name', 'author__first_name', 'author__last_name', 'event_location', 'date',)

    ordering = ['date']
    filter_horizontal = ()
    
    change_fieldsets = (
        ('Event Info', {'fields': ('name', 'author')}),
        ('Event Description', {'fields': ('text', 'file')}),
        ('Location and Time', {'fields': ('date', 'event_location')}),
    )
    
    add_fieldsets = (
        ('Event Info', {'fields': ('name', )}),
        ('Event Description', {'fields': ('text', 'file')}),
        ('Location and Time', {'fields': ('date', 'event_location')}),
    )
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            form = self.change_form
            return form
    
    pass
    
admin.site.register(Event, EventAdmin)