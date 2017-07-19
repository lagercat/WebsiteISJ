from haystack import indexes


class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    suggestions = indexes.FacetCharField()
    text_auto = indexes.EdgeNgramField(model_attr='getAutocompleteText')

    class Meta:
        abstract = True

    def prepare(self, obj):
        prepared_data = super(BaseIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
