import random

import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.utils import translation
from django_consent import models


@pytest.mark.django_db
def test_base(user_consent):
    """
    This is the most basic of all tests, inheriting some fixtures
    """
    assert models.ConsentSource.objects.all().count() > 0
    assert models.UserConsent.objects.all().count() > 0

    assert str(models.ConsentSource.objects.all()[0])
    assert str(models.UserConsent.objects.all()[0])


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


@pytest.mark.django_db
def test_translations(user_consent):
    """
    Opt out some of the emails that have been created and check that they don't
    figure anywhere
    """
    for consent_source in models.ConsentSource.objects.all():

        # Test the __str__method
        str(consent_source)

        for consent_translation in consent_source.translations.all():
            # Test the __str__method
            str(consent_translation)

        with translation.override("404"):

            assert (
                str(consent_source.definition_translated) == consent_source.definition
            )
            assert (
                str(consent_source.source_name_translated) == consent_source.source_name
            )

        # Hindi exists
        assert any([x[0] == "hi" for x in settings.LANGUAGES])
        with translation.override("hi"):

            assert (
                str(consent_source.definition_translated) != consent_source.definition
            )
            assert (
                str(consent_source.source_name_translated) != consent_source.source_name
            )


@pytest.mark.django_db
@override_settings(USE_I18N=False)
def test_no_translations(user_consent):
    """
    Opt out some of the emails that have been created and check that they don't
    figure anywhere
    """
    for consent_source in models.ConsentSource.objects.all():
        str(consent_source)
        str(consent_source)

        assert str(consent_source.definition_translated) == consent_source.definition
        assert str(consent_source.source_name_translated) == consent_source.source_name
