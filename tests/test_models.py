import pytest
from django_consent import models


@pytest.fixture
def base_consent():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return {
        "consent_source": models.EmailConsentSources.objects.create(
            source_name="test",
            definition="Testing stuff",
        )
    }


@pytest.mark.django_db
def test_content(base_consent):
    """Sample pytest test function with the pytest fixture as an argument."""
    assert base_consent["consent_source"].id > 0
