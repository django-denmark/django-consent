from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django_consent.views import ConsentConfirmationSentView
from django_consent.views import ConsentCreateView


class Index(TemplateView):
    template_name = "base.html"


class ConsentCreateView(ConsentCreateView):
    template_name = "signup.html"

    def get_success_url(self):
        return reverse(
            "demo:signup_confirmation", kwargs={"source_id": self.consent_source.id}
        )


class ConsentConfirmationSentView(ConsentConfirmationSentView):
    pass
