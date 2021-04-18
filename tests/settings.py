# You may need more or less than what's shown here - this is a skeleton:
from django.utils.translation import gettext_lazy as _

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django_consent",
)

ROOT_URLCONF = "tests.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": ["path/to/your/templates"],
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SECRET_KEY = "this is a test"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

SITE_ID = 1

USE_I18N = True
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", _("English")),
    ("hi", _("Hindi")),
]
