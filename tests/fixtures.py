import random
import string
import uuid

import pytest
from django_consent import models


def get_random_string(length):
    return "".join(random.choice(string.ascii_letters) for __ in range(length))


def get_random_email():
    return (
        get_random_string(20)
        + "@"
        + get_random_string(10)
        + "."
        + random.choice(["org", "com", "gov.uk"])
    )


@pytest.fixture
def base_consent():
    """Pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return models.ConsentSource.objects.create(
        source_name="test",
        definition="Testing stuff",
    )


@pytest.fixture
def user_consent(base_consent):
    """Pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    user_consents = []
    for source in models.ConsentSource.objects.all():
        for __ in range(10):
            user_consents.append(
                models.UserConsent.capture_email_consent(
                    source, get_random_email(), require_confirmation=False
                )
            )

    return {
        "base_consent": base_consent,
        "user_consents": user_consents,
    }


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        kwargs["email"] = get_random_email()
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user
