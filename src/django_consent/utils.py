import uuid

from django.core import signing

from . import settings as consent_settings


def get_email_hash(email):
    return uuid.uuid3(uuid.NAMESPACE_URL, email)


def get_unsubscribe_token(consent):
    """
    Returns a token (for a URL) which can be validated to unsubscribe from the
    supplied consent object.
    """
    return signing.dumps(
        str(consent.email_hash) + "," + str(consent.id),
        salt=consent_settings.UNSUBSCRIBE_SALT,
    )


def validate_unsubscribe_token(token, consent):
    """
    Returns true/false according to whether the token validates for the consent
    object
    """
    try:
        value = signing.loads(
            token,
            salt=consent_settings.UNSUBSCRIBE_SALT,
        ).split(",")
        return value[0] == str(consent.email_hash) and value[1] == str(consent.id)
    except (signing.BadSignature, IndexError):
        return False
