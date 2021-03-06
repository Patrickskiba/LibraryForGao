"""
Base view classes for all registration workflows.

"""

from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from registration import signals
from registration.forms import RegistrationForm

from django.shortcuts import render

from books.models import Book

import datetime

class RegistrationView(FormView):
    """
    Base class for user registration views.

    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    success_url = None
    template_name = 'registration/registration_form.html'

    def dispatch(self, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.

        """
        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def register(self, form):
        """
        Implement user-registration logic here. Access to both the
        request and the registration form is available here.

        """
        raise NotImplementedError


class ActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    template_name = 'registration/activate.html'

    def get(self, *args, **kwargs):
        """
        The base activation logic; subclasses should leave this method
        alone and implement activate(), which is called from this
        method.

        """
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=self.request)
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(*args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        """
        Implement this to return the URL (either a 3-tuple for
        redirect(), or a simple string name of a URL pattern) to
        redirect to after successful activation.

        This differs from most get_success_url() methods of Django
        views in that it receives an extra argument: the user whose
        account was activated.

        """
        raise NotImplementedError


def profile(request):
    user = str(request.user)
    book_list = list(Book.objects.filter(checked_out_by=user))
    overdue = list(Book.objects.filter(return_date__lt=datetime.datetime.now(), checked_out_by=user))
    now = datetime.datetime.now().replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
    now = now.strftime('%m/%d/%Y')
    for LBook in book_list:
        if LBook.return_date < now:
            LBook.return_date = LBook.return_date + " -- It is late!!"
    context = {'book_list': book_list, 'book_list_overdue': overdue}
    return render(request, 'registration/profile.html', context)