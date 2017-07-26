from django.contrib.admin.filters import DateFieldListFilter

from news.forms import NewsChangeFormAdmin, NewsCreationFormAdmin
from utility.admin import AdminChangeMixin, register_model_admin

from .models import News


class NewsAdmin(AdminChangeMixin):    
    change_form = NewsChangeFormAdmin
    add_form = NewsCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"
    
    icon = '<i class="material-icons">rss_feed</i>'

    list_display = ('short_name', 'author', 'date', 'slug',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'author')}),
        ('News content', {'fields': ('text', 'file')})
    )
    
    add_fieldsets = (
        ('Page', {'fields': ('name',)}),
        ('News content', {'fields': ('text', 'file')})
    )
    
    search_fields = ('author__first_name', 'author__last_name', 'name', 'date', 'slug',)

    ordering = ['date']
    filter_horizontal = ()
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            form = self.change_form
            form.text_initial = obj.text
            return form
    
    pass

register_model_admin(News, NewsAdmin)
