from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from ratelimit.decorators import ratelimit

from . import forms
from . import models
from . import settings as consent_settings
from . import utils
from .settings import RATELIMIT


class ConsentCreateView(CreateView):
    """
    The view isn't part of urls.py but you can add it to your own project's
    url configuration if you want to use it.

    To mount it, add a source_id kwarg, for instance::

        path("signup/<int:source_id>/", SignupView.as_view()),
    """

    model = models.UserConsent
    form_class = forms.EmailConsentForm
    template_name = "consent/user/create.html"

    @method_decorator(ratelimit(key="ip", rate=RATELIMIT))
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

    def form_valid(self, form):
        ret_value = super().form_valid(form)
        consent = self.object
        consent.email_confirmation(request=self.request)
        return ret_value

    def get_success_url(self):
        """
        This requires a project with a urlconf specifying a view with the name
        'signup_confirmation'.
        """
        return reverse(
            "signup_confirmation", kwargs={"source_id": self.consent_source.id}
        )


class UserConsentActionView(DetailView):
    """
    An abstract view

    Validates that a token is valid for consent ID + email_hash
    """

    model = models.UserConsent
    context_object_name = "consent"
    token_salt = consent_settings.UNSUBSCRIBE_SALT

    @method_decorator(ratelimit(key="ip", rate=RATELIMIT))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def action(self, consent):
        raise NotImplementedError("blah")

    def get_object(self, queryset=None):
        consent = super().get_object(queryset)
        token = self.kwargs.get("token")

        if utils.validate_token(token, consent, salt=self.token_salt):
            self.action(consent)
            return consent
        else:
            raise Http404("This does not work")

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["token"] = utils.get_consent_token(c["consent"], salt=self.token_salt)
        return c


class ConsentWithdrawView(UserConsentActionView):
    """
    Withdraws a consent. In the case of a newsletter, it unsubscribes a user
    from receiving the newsletter.

    Requires a valid link with a token.
    """

    template_name = "consent/user/unsubscribe/done.html"
    model = models.UserConsent
    context_object_name = "consent"
    token_salt = consent_settings.UNSUBSCRIBE_SALT

    def action(self, consent):
        consent.optout()


class ConsentWithdrawUndoView(UserConsentActionView):
    """
    This is related to undoing withdrawal of consent in case that the user
    clicked the wrong link.

    Requires a valid link
    """

    template_name = "consent/user/unsubscribe/undo.html"
    token_salt = consent_settings.UNSUBSCRIBE_SALT

    def action(self, consent):
        consent.optouts.all().delete()


class ConsentWithdrawAllView(UserConsentActionView):
    """
    Withdraws a consent. In the case of a newsletter, it unsubscribes a user
    from receiving the newsletter.

    Requires a valid link with a token.
    """

    template_name = "consent/user/unsubscribe_all/done.html"
    model = models.UserConsent
    context_object_name = "consent"
    token_salt = consent_settings.UNSUBSCRIBE_ALL_SALT

    def action(self, consent):
        consent.optout(is_everything=True)


class ConsentWithdrawAllUndoView(UserConsentActionView):
    """
    This is related to undoing withdrawal of consent in case that the user
    clicked the wrong link.

    Requires a valid link

    This only cancels an withdrawal of everything that was related to this
    particular consent. Another withdrawal can still exist.
    """

    template_name = "consent/user/unsubscribe_all/undo.html"
    token_salt = consent_settings.UNSUBSCRIBE_ALL_SALT

    def action(self, consent):
        consent.optouts.filter(is_everything=True).delete()


class ConsentConfirmationReceiveView(UserConsentActionView):
    """
    Marks a consent as confirmed, this is important for items that require a
    confirmed email address.
    """

    template_name = "consent/user/confirmation_received.html"
    token_salt = consent_settings.CONFIRM_SALT

    def action(self, consent):
        consent.confirm()


class ConsentConfirmationSentView(TemplateView):
    """
    Informs a user that their confirmation has been sent
    """

    template_name = "consent/user/confirmation_sent.html"
