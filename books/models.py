from django.db import models


class Book(models.Model):
    book_title = models.CharField(max_length=250)
    book_author = models.CharField(max_length=150)
    book_isbn = models.CharField(max_length=100)
    checked_out_by = models.CharField(max_length=250)
    checked_out_date = models.CharField(max_length=250)
    return_date = models.CharField(max_length=250)

    def __str__(self):
        return "{0}, ID={1}".format(self.book_title, self.pk)
    class Meta:
         ordering = ['book_title']

