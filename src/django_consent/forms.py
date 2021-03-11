from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class EmailConsentForm(forms.ModelForm):
    """
    A simple model form to subscribe a user to a newsletter by storing their
    consent.

    To get a list of valid subscribers, simply do:

    models.ConsentSource.get(id=x).get_valid_consent()
    """

    def __init__(self, *args, **kwargs):
        self.consent_source = kwargs.pop("consent_source")
        super().__init__(*args, **kwargs)
        self.fields["consent_text"].initial = self.consent_source.definition

    email = forms.EmailField()

    consent_text = forms.CharField(
        widget=forms.Textarea(attrs={"disabled": True}), required=False
    )

    confirmation = forms.BooleanField(
        required=True, help_text=_("I consent to the above")
    )

    def save(self, commit=True):
        if not commit:
            raise RuntimeError("Not supported")
        return models.UserConsent.capture_email_consent(
            self.consent_source, self.cleaned_data["email"], require_confirmation=True
        )

    class Meta:
        model = models.UserConsent
        fields = []
