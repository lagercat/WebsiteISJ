from haystack import indexes

from gallery.models import Gallery


class GalleryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')

    def get_model(self):
        return Gallery
