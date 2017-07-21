from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from haystack.generic_views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet


class CustomSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet()
    form_class = SearchForm

    def buld_page(self):
        results = self.queryset
        paginator = Paginator(results, 4)

        page = self.request.GET.get('page')
        print page
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return (paginator, page)

    def get_context_data(self, *args, **kwargs):
        context = super(CustomSearchView, self).get_context_data(
            *args, **kwargs)
        context['suggestion'] = SearchQuerySet(
        ).spelling_suggestion(context['query'])
        paginator, page = self.buld_page()
        context['paginator'] = paginator
        context['page'] = page
        return context
