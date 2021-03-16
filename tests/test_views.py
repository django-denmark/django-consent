import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_consent import models
from django_consent import settings as consent_settings
from django_consent import utils

from .fixtures import get_random_email


@pytest.mark.django_db
def test_signup(client, user_consent):

    source = models.ConsentSource.objects.all().order_by("?")[0]
    url = reverse("signup", kwargs={"source_id": source.id})

    # Test render
    response = client.get(url)

    signup_email = get_random_email()

    data = {"email": signup_email, "confirmation": True}
    response = client.post(url, data=data)
    assert response.status_code == 302

    # Check that a user object exists with the email
    assert get_user_model().objects.get(email=signup_email)

    # Ensure that the email is NOT confirmed already
    assert not models.UserConsent.objects.get(
        user__email=signup_email, source_id=source.id
    ).is_valid()

    # Ensure that the email is NOT confirmed already
    assert not models.UserConsent.objects.get(
        user__email=signup_email, source_id=source.id
    ).email_confirmed


@pytest.mark.django_db
def test_signup_confirmation(client, user_consent):
    """
    Tests that the confirmation works after adding a new user, i.e. the page
    that says "please confirm your email".
    """
    source = models.ConsentSource.objects.all().order_by("?")[0]
    url = reverse("signup_confirmation", kwargs={"source_id": source.id})

    response = client.get(url)

    assert response.status_code == 200


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

    # Ensure that the email is confirmed already
    assert models.UserConsent.objects.get(
        user__email=user.email, source_id=source.id
    ).is_valid()


@pytest.mark.django_db
def test_signup_inactive_user(client, user_consent, create_user):
    """
    Test signing up someone that already exists but isn't active. Ensure that
    they are not automatically confirmed.
    """

    source = models.ConsentSource.objects.all().order_by("?")[0]
    url = reverse("signup", kwargs={"source_id": source.id})

    # Test render
    response = client.get(url)

    user = create_user()
    user.is_active = False
    user.save()

    data = {"email": user.email, "confirmation": True}
    response = client.post(url, data=data)
    assert response.status_code == 302

    # Ensure that the email is NOT confirmed already
    assert not models.UserConsent.objects.get(
        user__email=user.email, source_id=source.id
    ).is_valid()


@pytest.mark.django_db
def test_unsubscribe(client, user_consent, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.order_by("?")[0]

    url = reverse(
        "consent:unsubscribe",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.UNSUBSCRIBE_SALT
            ),
        },
    )
    url_undo = reverse(
        "consent:unsubscribe_undo",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.UNSUBSCRIBE_SALT
            ),
        },
    )

    # Test render
    response = client.get(url)
    assert response.status_code == 200
    assert not models.UserConsent.objects.get(id=consent.id).is_valid()
    assert url_undo in str(response.content)


@pytest.mark.django_db
def test_unsubscribe_undo(client, user_consent, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.order_by("?")[0]

    # Confirm this consent in case it's unconfirmed
    consent.confirm()

    url = reverse(
        "consent:unsubscribe_undo",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.UNSUBSCRIBE_SALT
            ),
        },
    )

    # Test render
    response = client.get(url)
    assert response.status_code == 200
    assert models.UserConsent.objects.get(id=consent.id).is_valid()


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


@pytest.mark.django_db
def test_unsubscribe_all(client, many_consents_per_user, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.order_by("?")[0]

    url = reverse(
        "consent:unsubscribe_all",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.UNSUBSCRIBE_ALL_SALT
            ),
        },
    )
    url_undo = reverse(
        "consent:unsubscribe_all_undo",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.UNSUBSCRIBE_ALL_SALT
            ),
        },
    )

    # Test render
    response = client.get(url)
    assert response.status_code == 200
    assert not models.UserConsent.objects.get(id=consent.id).is_valid()
    assert url_undo in str(response.content)


@pytest.mark.django_db
def test_unsubscribe_all_undo(client, many_consents_per_user, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.order_by("?")[0]

    # Confirm this consent in case it's unconfirmed
    consent.confirm()

    url = reverse(
        "consent:unsubscribe_all_undo",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.UNSUBSCRIBE_ALL_SALT
            ),
        },
    )

    # Test render
    response = client.get(url)
    assert response.status_code == 200
    assert models.UserConsent.objects.get(id=consent.id).is_valid()


@pytest.mark.django_db
def test_consent_confirm(client, user_consent, create_user):
    """Test that an unconfirmed consent is confirmed"""

    source = models.ConsentSource.objects.all().order_by("?")[0]

    consent = source.consents.filter(email_confirmed=False).order_by("?")[0]

    url = reverse(
        "consent:consent_confirm",
        kwargs={
            "pk": consent.id,
            "token": utils.get_consent_token(
                consent, salt=consent_settings.CONFIRM_SALT
            ),
        },
    )

    # Test render
    response = client.get(url)

    assert response.status_code == 200
    assert models.UserConsent.objects.get(id=consent.id).is_valid()
