import uuid


def get_email_hash(email):
    return uuid.uuid3(uuid.NAMESPACE_URL, email)
