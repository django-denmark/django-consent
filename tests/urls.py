"""
This urlconf exists so we can run tests without an actual
Django project (Django expects ROOT_URLCONF to exist.)
It is not used by installed instances of this app.
"""
from django.urls import include
from django.urls import path
from django_consent.views import SignupConfirmationView
from django_consent.views import SignupView

urlpatterns = [
    path("foo/", include("django_consent.urls")),
    path("signup/<int:source_id>/", SignupView.as_view(), name="signup"),
    path(
        "signup/<int:source_id>/confirmation/",
        SignupConfirmationView.as_view(),
        name="signup_confirmation",
    ),
    path("consent/", include("django_consent.urls")),
]
