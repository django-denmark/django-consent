import random

import pytest
from django_consent import models


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
