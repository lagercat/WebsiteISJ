from haystack.generic_views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet


class CustomSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet()
    form_class = SearchForm
