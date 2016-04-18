from django.http import Http404
from django.shortcuts import render

from .models import Book
# ...

def index(request):
    book_list = list(Book.objects.all())
    context = {'book_list': book_list}
    return render(request, 'books/index.html', context)

def detail(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/detail.html', {'book': book})

def rent(request, id):
    try:
        book = Book.objects.get(pk=id)
        book.checked_out_by = 1
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/rent.html', {'book': book})