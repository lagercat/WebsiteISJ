# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
from config import settings

from django.contrib import admin

from material.frontend.admin import ModuleAdmin

from .models import ModuleProxy
from .models import make_view_proxy


class AdminChangeMixin(admin.ModelAdmin):
    change_own_field = None
    change_own_owner_field = None
    can_change_own = True

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {
            "change": self.has_perm(request.user, "change"),
            "change_own": (self.has_perm(request.user, "change_own") and
                           self.can_change_own),
            "delete": self.has_perm(request.user, "delete"),
        }

    def has_perm(self, user, permission):
        """
            Usefull shortcut for `user.has_perm()`
        """
        if user.has_perm("%s.%s_%s" % (self.model._meta.app_label, permission,
                                       self.model.__name__.lower(),)):
            return True
        return False

    def has_module_permission(self, request):  # Django 1.8
        return True

    def has_add_permission(self, request, obj=None):
        return (self.has_perm(request.user, "add_own")
                and self.has_perm(request.user, 'change_own')
                and self.can_change_own) \
            or self.has_perm(request.user, 'change')

    def has_delete_permission(self, request, obj=None):
        return self.has_perm(request.user, "delete")

    def has_change_permission(self, request, obj=None):
        """
            Necessary permission check to let Django
            show change_form for `view` permissions
        """
        if self.has_perm(request.user, 'change'):
            return True
        elif self.has_perm(request.user, 'change_own') and self.can_change_own:
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
                    and (not hasattr(field, 'auto_now_add') or not field.auto_now_add) \
                    and (not hasattr(field, 'auto_now') or not field.auto_now) \
                    :
                all_model_fields.append(field.name)

        return self.readonly_fields

    def change_view(self, request, object_id, extra_context=None):
        """
            Disable buttons for `viewers` in `change_view`
        """
        extra_context = extra_context or {}
        extra_context['change'] = True
        extra_context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return admin.ModelAdmin.change_view(self, request, object_id, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = self.get_form(
            request, None).Meta.model._meta.verbose_name_plural
        if self.has_perm(request.user, 'change_own') and self.can_change_own and not self.has_perm(request.user, 'change'):
            extra_context['title'] = "Owned " + \
                self.get_form(
                    request, None).Meta.model._meta.verbose_name_plural
        return admin.ModelAdmin.changelist_view(self, request, extra_context=extra_context)

    def get_actions(self, request):
        actions = super(AdminChangeMixin, self).get_actions(request)
        return actions

    def get_queryset(self, request):
        queryset = admin.ModelAdmin.get_queryset(self, request)
        if self.has_perm(request.user, 'change_own') and self.can_change_own and not self.has_perm(request.user, 'change'):
            if self.change_own_field is None:
                raise "change_own_field must be set."
            if self.change_own_owner_field is None:
                raise "change_own_owner_field must be set."
            print getattr(request.user, self.change_own_owner_field)
            kwargs = {
                self.change_own_field: getattr(request.user, self.change_own_owner_field).id if self.change_own_field is 'id' else
                getattr(request.user, self.change_own_owner_field).all() if self.change_own_field[-4:] == "__in" else
                getattr(request.user, self.change_own_owner_field),
            }
            return queryset.filter(**kwargs)
        return queryset


class AdminViewMixin(admin.ModelAdmin):

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {
            "view": self.has_perm(request.user, "view") and not self.has_perm(request.user, "change"),
        }

    def has_perm(self, user, permission):
        """
            Usefull shortcut for `user.has_perm()`
        """
        if user.has_perm("%s.%s_%s" % (self.model._meta.app_label, permission, self.model.__name__.lower(),)):
            return True
        return False

    def has_module_permission(self, request):  # Django 1.8
        return True

    def has_change_permission(self, request, obj=None):
        """
            Necessary permission check to let Django show change_form for `view` permissions
        """
        if self.has_perm(request.user, 'view'):
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
                    and (not hasattr(field, 'auto_now_add') or not field.auto_now_add) \
                    and (not hasattr(field, 'auto_now') or not field.auto_now) \
                    :
                all_model_fields.append(field.name)

        return all_model_fields

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = self.get_form(
            request, None).Meta.model._meta.verbose_name_plural
        return admin.ModelAdmin.changelist_view(self, request, extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        """
            Disable buttons for `viewers` in `change_view`
        """
        extra_context = extra_context or {}
        extra_context['change'] = False
        extra_context['view'] = True
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_delete_link'] = False
        extra_context['title'] = "View " + \
            self.get_form(request, object_id).Meta.model._meta.verbose_name
        extra_context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return admin.ModelAdmin.change_view(self, request, object_id, extra_context=extra_context)

    def get_actions(self, request):
        actions = super(AdminViewMixin, self).get_actions(request)
        if actions.get('delete_selected', False):
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        queryset = admin.ModelAdmin.get_queryset(self, request)
        if self.has_perm(request.user, 'view'):
            kwargs = {
                self.change_own_field: getattr(request.user,
                                               self.change_own_owner_field).id if self.change_own_field is 'id' else getattr(
                    request.user, self.change_own_owner_field),
            }
            return queryset.exclude(**kwargs)
        return queryset


def make_view_admin(admin):
    class ViewAdmin(AdminViewMixin, admin):
        pass
    ViewAdmin.__name__ = admin.__name__
    return ViewAdmin


def register_model_admin(model, model_admin):
    admin.site.register(model, model_admin)
    admin.site.register(make_view_proxy(model), make_view_admin(model_admin))


def register_module_admin():
    print ModuleProxy.__name__
    admin.site.register(ModuleProxy, make_view_admin(ModuleAdmin))
