from haystack.generic_views import SearchView
from haystack.forms import SearchForm
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
