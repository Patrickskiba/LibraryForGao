from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render
from .models import Book
from haystack.query import SearchQuerySet
from django.db.models import Count
import datetime
# ...


def browse(request):
    book_list = Book.objects.filter(checked_out_by="null").distinct("book_title")
    paginator = Paginator(book_list, 20) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        bookPag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bookPag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        bookPag = paginator.page(paginator.num_pages)
    for book in bookPag:
        book.count = Book.objects.filter(checked_out_by="null").filter(book_title=book.book_title).count()
        book.save()

    context = {'book_list': bookPag}
    return render(request, 'books/browse.html', context)


def detail(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/detail.html', {'book': book})


def rent(request, id):
    try:
        book = Book.objects.get(pk=id)
        book.checked_out_by = str(request.user)

        now = datetime.datetime.now()
        now = now.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
        print(now)
        book.checked_out_date = now.strftime('%m/%d/%Y')
        book.return_date = (now + datetime.timedelta(days=14)).strftime('%m/%d/%Y')
        book.count = Book.objects.filter(checked_out_by="null").filter(book_title=book.book_title).count()
        book.save()

        book.save()
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/rent.html', {'book': book})

def search_titles(request):
    book_search = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ""))

    return render(request, 'books/results.html',  {'book_search': book_search})
