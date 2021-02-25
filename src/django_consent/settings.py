from django.conf import settings


#: You can harden security by adding a different salt in your project's settings
UNSUBSCRIBE_SALT = getattr(settings, "CONSENT_UNSUBSCRIBE_SALT", "django-consent")
