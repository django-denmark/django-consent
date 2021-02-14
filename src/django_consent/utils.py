import random
import string
import uuid


def get_email_hash(email):
    return uuid.uuid3(uuid.NAMESPACE_URL, email)


def get_anonymous_email():
    chars = string.ascii_uppercase + string.digits
    return "anonymized.{}@{}.anonymized.com".format(
        "".join(random.choice(chars) for _ in range(20)),
        "".join(random.choice(chars) for _ in range(20)),
    )
