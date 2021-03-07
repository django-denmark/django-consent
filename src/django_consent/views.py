from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from . import forms
from . import models
from . import utils


class SignupView(CreateView):
    """
    The view isn't part of urls.py but you can add it to your own project's
    url configuration if you want to use it.

    To mount it, add a source_id kwarg, for instance::

        path("signup/<int:source_id>/", SignupView.as_view()),
    """

    model = models.UserConsent
    form_class = forms.EmailConsentForm
    template_name = "consent/user/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.consent_source = get_object_or_404(
            models.ConsentSource, id=kwargs["source_id"]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["consent_source"] = self.consent_source
        return kwargs

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["consent_source"] = self.consent_source
        return c

    def get_success_url(self):
        return reverse(
            "signup_confirmation", kwargs={"source_id": self.consent_source.id}
        )


class SignupConfirmationView(TemplateView):
    """
    Tells the user to check their inbox after a successful signup.

    To mount it, add a source_id kwarg, for instance::

        path("signup/<int:source_id>/confirmation/", SignupConfirmationView.as_view()),
    """

    template_name = "consent/user/confirm.html"


class UserConsentActionView(DetailView):
    """
    An abstract view

    Validates that a token is valid for consent ID + email_hash
    """

    model = models.UserConsent
    context_object_name = "consent"

    def action(self, consent):
        raise NotImplementedError("blah")

    def get_object(self, queryset=None):
        consent = super().get_object(queryset)
        token = self.kwargs.get("token")

        if utils.validate_unsubscribe_token(token, consent):
            self.action(consent)
            return consent
        else:
            raise Http404("This does not work")

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["token"] = utils.get_unsubscribe_token(c["consent"])
        return c


class UnsubscribeConsentView(UserConsentActionView):
    """
    Unsubscribes a user from a given consent.

    Requires a valid link
    """

    template_name = "consent/user/unsubscribe/done.html"
    model = models.UserConsent
    context_object_name = "consent"

    def action(self, consent):
        consent.optout()


class UnsubscribeConsentUndoView(UserConsentActionView):
    """
    Unsubscribes a user from a given consent.

    Requires a valid link
    """

    template_name = "consent/user/unsubscribe/undo.html"

    def action(self, consent):
        consent.optouts.all().delete()


class SubscribeConsentConfirmView(UserConsentActionView):
    """
    Marks a consent as confirmed, this is important for items that require a
    confirmed email address.
    """

    template_name = "consent/user/confirm.html"

    def action(self, consent):
        consent.confirm()
