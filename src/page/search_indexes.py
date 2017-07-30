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
from haystack import indexes

from page.models import Article
from page.models import Category
from page.models import SimplePage
from page.models import Subcategory
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
    slug_sub = indexes.CharField(model_attr='slug_sub')
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
