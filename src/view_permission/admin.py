from django.contrib import admin

class AdminViewMixin(admin.ModelAdmin): 

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
        if self.has_perm(request.user,'change'):
            return True
        elif self.has_perm(request.user,'view'):
            return True
        return super(admin.ModelAdmin, self).has_change_permission(request, obj)

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
                
        if self.has_perm(request.user,'change'):
            return self.readonly_fields
        elif self.has_perm(request.user,'view'):
            return all_model_fields
        return self.readonly_fields

    def change_view(self, request, object_id, extra_context=None):
        """
            Disable buttons for `viewers` in `change_view`
        """

        if self.has_perm(request.user,'change'):
            pass
        elif self.has_perm(request.user,'view'):
            extra_context = extra_context or {}
            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
        return super(AdminViewMixin, self).change_view(request, object_id, extra_context=extra_context)
      
    def get_actions(self, request):
        actions = super(AdminViewMixin, self).get_actions(request)
        if self.has_perm(request.user,'change'):
            pass
        elif self.has_perm(request.user,'view'):
            del actions['delete_selected']
        return actions