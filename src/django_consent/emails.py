from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.template import loader
from django.utils.translation import gettext as _


class BaseEmail(EmailMessage):
    """
    Base class for sending emails
    """

    template = "consent/email/base.txt"
    subject_template = "consent/email/base_subject.txt"

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop("context", {})
        self.user = kwargs.pop("user", None)
        self.request = kwargs.pop("request", None)
        if self.user:
            kwargs["to"] = [self.user.email]
            self.context["user"] = self.user
            self.context["recipient_name"] = self.user.get_full_name()

        # Overwrite if recipient_name is set
        self.context["recipient_name"] = kwargs.pop(
            "recipient_name", self.context.get("recipient_name", None)
        )

        super(BaseEmail, self).__init__(*args, **kwargs)
        self.body = self.get_body()
        self.subject = self.get_subject()

    def get_context_data(self):
        c = self.context
        site = get_current_site(self.request)
        c["request"] = self.request
        c["domain"] = site.domain
        c["site_name"] = site.name
        c["protocol"] = "https" if not settings.DEBUG else "http"
        return c

    def get_body(self):
        return loader.render_to_string(self.template, self.get_context_data())

    def get_subject(self):
        # Remember the .strip() as templates often have dangling newlines which
        # are not accepted as subject lines
        return loader.render_to_string(
            self.subject_template, self.get_context_data()
        ).strip()

    def send_with_feedback(self, success_msg=None):
        if not success_msg:
            success_msg = _("Email successfully sent to {}".format(", ".join(self.to)))
        try:
            self.send(fail_silently=False)
            messages.success(self.request, success_msg)
        except RuntimeError:
            messages.error(
                self.request, _("Not sent, something wrong with the mail server.")
            )


class ConfirmationNeededEmail(BaseEmail):
    """
    Email sent to confirm the validity of an email in connection to a consent
    that was given.
    """

    template = "consent/email/confirmation.txt"
    subject_template = "consent/email/confirmation_subject.txt"

    def __init__(self, *args, **kwargs):

        self.consent = kwargs.pop("consent")
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        c = super().get_context_data()
        c["consent"] = self.consent
        return c
