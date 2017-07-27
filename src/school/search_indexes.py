from haystack import indexes

from school.models import School


class SchoolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    file = indexes.CharField(model_attr='file')
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return School

    def prepare(self, obj):
        prepared_data = super(SchoolIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
