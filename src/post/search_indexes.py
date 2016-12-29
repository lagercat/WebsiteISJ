from haystack import indexes

from models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    author = indexes.CharField(model_attr='user')

    def get_model(self):
        return Post

    def index_queryset(self, using=Post):
        return self.get_model().objects.all()