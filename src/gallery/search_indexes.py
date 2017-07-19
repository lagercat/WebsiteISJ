from haystack import indexes

from gallery.models import Gallery
from search.search_indexes import BaseIndex


class EventIndex(BaseIndex, indexes.Indexable):

    def get_model(self):
        return Gallery
