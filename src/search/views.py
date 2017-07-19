import simplejson as json

from django.http import HttpResponse

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


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
        content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
