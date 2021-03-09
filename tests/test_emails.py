import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sites.models import Site
from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django_consent import emails
from django_consent import models


class FailBackend(BaseEmailBackend):
    """
    This backend loves failing :)
    """

    def send_messages(self, messages):
        raise RuntimeError("I blow up 🤯")


@pytest.mark.django_db
def test_base(user_consent, rf):
    """
    This does a pretty basic test, and should be split up a bit.

    We should cover some more cases, as we cannot say for sure yet if we know
    for instance the name of the recipient.
    """
    request = rf.get("/")

    # Add messages and session to request object
    # https://stackoverflow.com/questions/23861157/how-do-i-setup-messaging-and-session-middleware-in-a-django-requestfactory-durin
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)

    # Because the default Site object uses example.com and a request object
    # from django RequestFactory generates testserver
    Site.objects.all().update(domain=request.get_host())
    user = models.UserConsent.objects.all().order_by("?")[0].user
    email = emails.BaseEmail(request=request, user=user)
    email.send()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Django Consent"

    email.send_with_feedback()
    assert len(mail.outbox) == 2

    email.connection = FailBackend()
    email.send_with_feedback()
    assert len(mail.outbox) == 2  # No increment expected

    email = emails.BaseEmail(request=request, user=user, recipient_name="test person")
    email.send()
    assert len(mail.outbox) == 3
    assert "test person" in mail.outbox[-1].body


@pytest.mark.django_db
def test_confirm(user_consent):
    consent = models.UserConsent.objects.filter(email_confirmed=False).order_by("?")[0]
    consent.email_confirmation(request=None)
    assert len(mail.outbox) == 1
    assert "Your confirmation is needed" in mail.outbox[-1].subject
