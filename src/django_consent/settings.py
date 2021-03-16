from django.conf import settings


#: You can harden security by adding a different salt in your project's settings
UNSUBSCRIBE_SALT = getattr(
    settings, "CONSENT_UNSUBSCRIBE_SALT", "django-consent-unsubscribe"
)

#: You can harden security by adding a different salt in your project's settings
UNSUBSCRIBE_ALL_SALT = getattr(
    settings, "CONSENT_UNSUBSCRIBE_SALT", "django-consent-unsubscribe-all"
)

#: You can harden security by adding a different salt in your project's settings
CONFIRM_SALT = getattr(settings, "CONSENT_CONFIRM_SALT", "django-consent-confirm")

#: For more information, `django-ratelimit <https://django-ratelimit.readthedocs.io/en/stable/>`__
RATELIMIT = getattr(settings, "CONSENT_RATELIMIT", "100/h")
