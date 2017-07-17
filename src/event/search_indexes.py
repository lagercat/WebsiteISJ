from haystack import indexes

from event.models import Event
from post.search_indexes import BaseIndex


class EventIndex(BaseIndex, indexes.Indexable):

    def get_model(self):
        return Event
