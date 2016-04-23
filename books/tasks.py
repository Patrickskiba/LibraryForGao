from celery import task
from django.core.mail import send_mail
from django.contrib.auth.models import User
import time
from .models import Book
import datetime

@task()
def emailLateUsers():
    checked_out = Book.objects.exclude(checked_out_by="null")
    for item in checked_out:
        _parsed = datetime.datetime.strptime(str(item.return_date),"%Y-%m-%d %H:%M:%S.%f")
        if((_parsed) > datetime.datetime.now()):
            deviant = User.objects.get(username= item.checked_out_by)
            message = "Hello {0}, you are recieving this email because the book: {1} is over due. \nPlease return it, we know where you live and we will find you. This will be your last warning. Failure to return the book will result in enrollment in our re-education program.".format(deviant.first_name, item.book_title)
            send_mail('Subject', message, 'libraryforgao@gmail.com',[deviant.email])
            time.sleep(10)
