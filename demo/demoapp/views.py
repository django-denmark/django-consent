from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django_consent.views import SignupConfirmationView
from django_consent.views import SignupView


class Index(TemplateView):
    template_name = "base.html"


class SignupView(SignupView):
    template_name = "signup.html"

    def get_success_url(self):
        return reverse(
            "demo:signup_confirmation", kwargs={"source_id": self.consent_source.id}
        )


class SignupConfirmationView(SignupConfirmationView):
    pass
