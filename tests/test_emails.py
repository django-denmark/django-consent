import pytest
from django.contrib.sites.models import Site
from django.core import mail
from django_consent import emails
from django_consent import models


@pytest.mark.django_db
def test_base(user_consent, rf):
    request = rf.get("/")
    # Because the default Site object uses example.com and a request object
    # from django RequestFactory generates testserver
    Site.objects.all().update(domain=request.get_host())
    user = models.UserConsent.objects.all().order_by("?")[0].user
    email = emails.BaseEmail(request, user=user)
    email.send()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Django Consent"
