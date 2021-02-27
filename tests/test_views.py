import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_consent import models
from django_consent import utils

from .fixtures import get_random_email


@pytest.mark.django_db
def test_signup(client, user_consent):

    source = models.ConsentSource.objects.all().order_by("?")[0]
    url = reverse("signup", kwargs={"source_id": source.id})

    # Test render
    response = client.get(url)

    singup_email = get_random_email()

    data = {"email": singup_email, "confirmation": True}
    response = client.post(url, data=data)
    assert response.status_code == 302

    # Check that a user object exists with the email
    assert get_user_model().objects.get(email=singup_email)


@pytest.mark.django_db
def test_signup_active_user(client, user_consent, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]
    url = reverse("signup", kwargs={"source_id": source.id})

    # Test render
    response = client.get(url)

    user = create_user()

    data = {"email": user.email, "confirmation": True}
    response = client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_unsubscribe(client, user_consent, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.order_by("?")[0]

    url = reverse(
        "consent:unsubscribe",
        kwargs={
            "pk": consent.id,
            "token": utils.get_unsubscribe_token(consent),
        },
    )

    # Test render
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_unsubscribe_invalid(client, user_consent, create_user):
    """Test that an invalid token returns 404"""

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.order_by("?")[0]

    url = reverse(
        "consent:unsubscribe",
        kwargs={"pk": consent.id, "token": "invalid"},
    )

    # Test render
    response = client.get(url)

    assert response.status_code == 404
