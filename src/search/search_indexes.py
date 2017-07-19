from haystack import indexes

from custom_index import CustomNgramField


class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = CustomNgramField(model_attr='name',
                            index_analyzer='analyzer_1',
                            search_analyzer='analyzer_2')
    slug = indexes.CharField(model_attr='slug')

    class Meta:
        abstract = True
