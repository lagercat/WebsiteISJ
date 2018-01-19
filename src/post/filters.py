from django.contrib.admin.filters import AllValuesFieldListFilter
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import ValidationError


class FileLocationFilter(AllValuesFieldListFilter):

    def queryset(self, request, queryset):
        try:
            if not self.used_parameters:
                return queryset.filter(location='interior')
            return queryset.filter(**self.used_parameters)
        except (ValueError, ValidationError) as e:
            raise IncorrectLookupParameters(e)
