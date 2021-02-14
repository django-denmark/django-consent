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
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    models.ConsentSource.objects.create(
        source_name="test",
        definition="Testing stuff",
    )


@pytest.fixture
def email_consent(base_consent):
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    for source in models.ConsentSource.objects.all():
        for __ in range(10):
            models.EmailConsent.capture_email_consent(
                source=source,
                email=get_random_email(),
            )


@pytest.mark.django_db
def test_content(email_consent):
    """Sample pytest test function with the pytest fixture as an argument."""
    assert models.ConsentSource.objects.all().count() > 0
    assert models.EmailConsent.objects.all().count() > 0
