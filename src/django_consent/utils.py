import uuid

from django.core.signing import Signer

from . import settings as consent_settings


def get_email_hash(email):
    return uuid.uuid3(uuid.NAMESPACE_URL, email)


def get_unsubscribe_token(email_hash, consent_id):
    return Signer().sign(
        email_hash + str(consent_id), salt=consent_settings.UNSUBSCRIBE_SALT
    )
