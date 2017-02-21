from django.contrib import admin
from config import settings
from .models import make_view_proxy

class AdminChangeMixin(admin.ModelAdmin): 
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {
            "change" : self.has_perm(request.user, "change"), 
            "change_own" : self.has_perm(request.user, "change_own"),
            "delete" : self.has_perm(request.user, "change"), 
        }
      
    def has_perm(self, user, permission):
        """
            Usefull shortcut for `user.has_perm()`
        """
        if user.has_perm("%s.%s_%s" % (self.model._meta.app_label,permission,self.model.__name__.lower(),)):
            return True
        return False

    def has_module_permission(self, request): # Django 1.8
        return True

    def has_add_permission(self, request, obj=None):
        return self.has_perm(request.user, "change") or self.has_perm(request.user, "change_own")

    def has_delete_permission(self, request, obj=None):
        return self.has_perm(request.user, "change") or self.has_perm(request.user, "change_own")

    def has_change_permission(self, request, obj=None):
        """
            Necessary permission check to let Django show change_form for `view` permissions
        """
        if self.has_perm(request.user,'change'):
            return True
        elif self.has_perm(request.user,'change_own'):
            return True        
        return False

    def get_readonly_fields(self, request, obj=None):
        """
            Turn each model field into read-only for `viewers`
        """
        all_model_fields = []
        for field in self.model._meta.fields:
            # TODO in Django 1.8 use ModelAdmin.get_fields()
            if not field.auto_created \
                and (not hasattr(field,'auto_now_add') or not field.auto_now_add) \
                and (not hasattr(field,'auto_now') or not field.auto_now) \
                :
                all_model_fields.append(field.name)
                
        return self.readonly_fields

    def change_view(self, request, object_id, extra_context=None):
        """
            Disable buttons for `viewers` in `change_view`
        """
        extra_context = extra_context or {}
        extra_context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return super(AdminChangeMixin, self).change_view(request, object_id, extra_context=extra_context)
      
    def get_actions(self, request):
        actions = super(AdminChangeMixin, self).get_actions(request)
        return actions
      
    def get_queryset(self, request):
      queryset = admin.ModelAdmin.get_queryset(self, request)
      if self.has_perm(request.user,'change_own') and not self.has_perm(request.user,'change'):
          return queryset.filter(author=request.user)
      return queryset
      
class AdminViewMixin(admin.ModelAdmin): 
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {
            "view" : self.has_perm(request.user, "view") and not self.has_perm(request.user, "change"), 
        }
        
    def has_perm(self, user, permission):
        """
            Usefull shortcut for `user.has_perm()`
        """
        if user.has_perm("%s.%s_%s" % (self.model._meta.app_label,permission,self.model.__name__.lower(),)):
            return True
        return False

    def has_module_permission(self, request): # Django 1.8
        return True

    def has_change_permission(self, request, obj=None):
        """
            Necessary permission check to let Django show change_form for `view` permissions
        """    
        if self.has_perm(request.user,'view'):
            return True
        return False
      
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        """
            Turn each model field into read-only for `viewers`
        """
        all_model_fields = []
        for field in self.model._meta.fields:
            # TODO in Django 1.8 use ModelAdmin.get_fields()
            if not field.auto_created \
                and (not hasattr(field,'auto_now_add') or not field.auto_now_add) \
                and (not hasattr(field,'auto_now') or not field.auto_now) \
                :
                all_model_fields.append(field.name)
        
        return all_model_fields


    def change_view(self, request, object_id, extra_context=None):
        """
            Disable buttons for `viewers` in `change_view`
        """
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_delete_link'] = False
        extra_context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return super(AdminViewMixin, self).change_view(request, object_id, extra_context=extra_context)
      
    def get_actions(self, request):
        actions = super(AdminViewMixin, self).get_actions(request)
        del actions['delete_selected']
        return actions
      
def make_view_admin(admin):   
    class ViewAdmin(AdminViewMixin, admin):
        pass
    ViewAdmin.__name__ = admin.__name__
    return ViewAdmin
  
def register_model_admin(model, model_admin):
    admin.site.register(model, model_admin)
    admin.site.register(make_view_proxy(model), make_view_admin(model_admin))