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
    models.ConsentSource.objects.create(
        source_name="test",
        definition="Testing stuff",
    )


@pytest.fixture
def email_consent(base_consent):
    """Pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    for source in models.ConsentSource.objects.all():
        for __ in range(10):
            models.EmailConsent.capture_email_consent(
                source=source,
                email=get_random_email(),
            )


def test_base(email_consent):
    """
    This is the most basic of all tests, inheriting some fixtures
    """
    assert models.ConsentSource.objects.all().count() > 0
    assert models.EmailConsent.objects.all().count() > 0


@pytest.mark.django_db
def test_optout_filters(email_consent):
    """
    Opt out some of the emails that have been created and check that they don't
    figure anywhere
    """
    pass
