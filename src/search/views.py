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
from haystack.forms import SearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet


class CustomSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet()
    form_class = SearchForm

    def get_context_data(self, *args, **kwargs):
        context = super(CustomSearchView, self).get_context_data(
            *args, **kwargs)
        context['suggestion'] = SearchQuerySet(
        ).spelling_suggestion(context['query'])
        return context
