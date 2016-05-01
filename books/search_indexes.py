from haystack import indexes
from books.models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='book_author')


    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(checked_out_by="null").distinct("book_title")

