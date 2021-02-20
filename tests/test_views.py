import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_consent import models

from .fixtures import get_random_email


@pytest.mark.django_db
def test_view(client, user_consent):

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
def test_view_active_user(client, user_consent, create_user):

    source = models.ConsentSource.objects.all().order_by("?")[0]
    url = reverse("signup", kwargs={"source_id": source.id})

    # Test render
    response = client.get(url)

    user = create_user()

    data = {"email": user.email, "confirmation": True}
    response = client.post(url, data=data)
    assert response.status_code == 302
