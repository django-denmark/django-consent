import random
import string

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
                    source=source,
                    email=get_random_email(),
                )
            )

    return {
        "base_consent": base_consent,
        "user_consents": user_consents,
    }


@pytest.mark.django_db
def test_base(user_consent):
    """
    This is the most basic of all tests, inheriting some fixtures
    """
    assert models.ConsentSource.objects.all().count() > 0
    assert models.UserConsent.objects.all().count() > 0


@pytest.mark.django_db
def test_optout_filters(user_consent):
    """
    Opt out some of the emails that have been created and check that they don't
    figure anywhere
    """
    optouts_to_create = 5
    consent_to_optout = random.sample(
        list(models.UserConsent.objects.all()), optouts_to_create
    )

    for consent in consent_to_optout:
        consent.optout()

    assert optouts_to_create == models.EmailOptOut.objects.count()

    assert user_consent["base_consent"].get_valid_consent().count() == (
        models.UserConsent.objects.all().count() - optouts_to_create
    )
