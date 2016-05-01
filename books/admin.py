from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("book_title","checked_out_by")
    list_filter = ("checked_out_by", )
    class Meta:
        model = Book



admin.site.register(Book, BookAdmin)
