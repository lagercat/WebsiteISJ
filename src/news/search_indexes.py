from haystack import indexes

from news.models import News
from search.search_indexes import BaseIndex


class NewsIndex(BaseIndex, indexes.Indexable):

    def get_model(self):
        return News
