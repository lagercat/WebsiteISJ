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

    def prepare(self, obj):
        prepared_data = super(BaseIndex, self).prepare(obj)
        print prepared_data
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
