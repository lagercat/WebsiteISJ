from haystack import indexes

from subject.models import Subcategory, SubjectPost
from search.search_indexes import BaseIndex


class SubcategoryIndex(BaseIndex, indexes.Indexable):
    subject = indexes.CharField(model_attr="subject")

    def get_model(self):
        return Subcategory


class SubjectPostIndex(BaseIndex, indexes.Indexable):
    subject = indexes.CharField(model_attr="subject")

    def get_model(self):
        return SubjectPost
