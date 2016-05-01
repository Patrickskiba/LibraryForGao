from django.db import models

class Book(models.Model):
    book_title = models.CharField(max_length=250)
    book_author = models.CharField(max_length=150)
    book_isbn = models.CharField(max_length=100)
    book_img = models.CharField(max_length=1000)
    checked_out_by = models.CharField(max_length=250)
    checked_out_date = models.CharField(max_length=250)
    return_date = models.CharField(max_length=250)
    count = models.CharField(max_length=400)


    def __str__(self):
        return "{0}, ID={1}, Checked out by: {2}".format(self.book_title, self.pk, self.checked_out_by)
    class Meta:
         ordering = ['book_title']

