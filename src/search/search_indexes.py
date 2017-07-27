from haystack import indexes


class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    file = indexes.CharField(model_attr='file')
    suggestions = indexes.FacetCharField()

    class Meta:
        abstract = True

    def prepare(self, obj):
        prepared_data = super(BaseIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
