from haystack import indexes

from page.models import Category, Subcategory, Article, SimplePage
from search.search_indexes import BaseIndex


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    slug = indexes.CharField(model_attr='slug')
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Category

    def prepare(self, obj):
        prepared_data = super(CategoryIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data


class SubcategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug_sub')
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Subcategory

    def prepare(self, obj):
        prepared_data = super(SubcategoryIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data


class ArticleIndex(BaseIndex, indexes.Indexable):
    subcategory = indexes.CharField(model_attr='subcategory')

    def get_model(self):
        return Article


class SimplePageIndex(BaseIndex, indexes.Indexable):

    def get_model(self):
        return SimplePage
