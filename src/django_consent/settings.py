from django.conf import settings


#: You can harden security by adding a different salt in your project's settings
UNSUBSCRIBE_SALT = getattr(
    settings, "CONSENT_UNSUBSCRIBE_SALT", "django-consent-unsubscribe"
)

#: You can harden security by adding a different salt in your project's settings
CONFIRM_SALT = getattr(settings, "CONSENT_CONFIRM_SALT", "django-consent-confirm")
