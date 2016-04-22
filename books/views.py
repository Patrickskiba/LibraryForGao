from django.http import Http404
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Book
import time
import datetime
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
        book.checked_out_by = str(request.user)

        now = datetime.datetime.now()
        book.checked_out_date = now
        book.return_date = now + datetime.timedelta(days=14)  # rental will last 2 weeks (aka 14 days)

        book.save()
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/rent.html', {'book': book})


def emailLateUsers(request):
    checked_out = Book.objects.exclude(checked_out_by="null")
    for item in checked_out:
        _parsed = datetime.datetime.strptime(str(item.return_date),"%Y-%m-%d %H:%M:%S.%f")
        if((_parsed) > datetime.datetime.now()):
            message = "Hello, you are recieving this email because the book: {0} is over due. \n Please return it, we know where you live and we will find you. This will be your last warning. Failure to return the book will result in enrollment in our re-education program.".format(item.book_title)
            send_mail('Subject', message, 'libraryforgao@gmail.com',['superninja234@gmail.com'])
            time.sleep(15)
    return render(request, 'books/success.html')
