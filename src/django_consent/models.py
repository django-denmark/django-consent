from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.utils import get_random_secret_key
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import emails
from . import settings as consent_settings
from . import utils


class ConsentSource(models.Model):
    """
    A consent source always has to be present when adding email addresses. It
    should clearly specify how we imagine that the user opted in.

    Specific events for specific users could be captured as well, but we intend
    to start out a bit less dramatic.

    Notice that some consent sources may change their meaning over time. For
    instance, someone can sign up as a member and continue to receive certain
    email updates despite their membership expiring.

    In a different case, the consent may be implicit because the email is
    mandatory: For instance password reminders, membership confirmations,
    confirmations of website actions etc.
    """

    source_name = models.CharField(max_length=255)
    definition = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    requires_confirmed_email = models.BooleanField(default=False)
    requires_active_user = models.BooleanField(default=False)

    def get_valid_consent(self):
        """
        Returns all current consent (that have not opted out)
        """
        return (
            UserConsent.objects.filter(source=self)
            .exclude(user__email_optouts__is_everything=True)
            .exclude(optouts__user=F("user"))
            .exclude(optouts__email_hash=F("email_hash"))
            .filter(
                Q(source__requires_confirmed_email=False) | Q(email_confirmed=True),
                Q(source__requires_active_user=False) | Q(user__is_active=True),
            )
        ).distinct()

    def __str__(self):
        return self.source_name


class UserConsent(models.Model):
    """
    Specifies the consent of a user to receive emails and what source the
    consent originated from.

    Usually, the source will also clarify which emails we MAY send.

    Anonymization: If a user is deleted, all their consents are also deleted as
    well.
    """

    source = models.ForeignKey(
        ConsentSource, on_delete=models.CASCADE, related_name="consents"
    )
    user = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    email_confirmation_requested = models.DateTimeField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    email_hash = models.UUIDField()

    def email_confirmation(self, request=None):
        """
        Sends a confirmation email if necessary
        """
        if not self.email_confirmed:
            email = emails.ConfirmationNeededEmail(
                request=request, user=self.user, consent=self
            )
            email.send()
            self.email_confirmation_requested = timezone.now()
            self.save()

    def __str__(self):
        return "{} agrees to {}".format(self.email, self.source.source_name)

    @classmethod
    def capture_email_consent(cls, source, email, require_confirmation=False):
        """
        Stores consent for a specific email.

        :param: require_confirmation: If set, creating consent for an email
        address that does not exist, will require the user to confirm their
        consent.
        """
        User = get_user_model()
        # Field values for creating the new UserConsent object
        consent_create_kwargs = {
            "email_confirmed": not require_confirmation,
        }

        try:
            user = User.objects.get(**{User.EMAIL_FIELD: email})
            if not user.is_active and require_confirmation:
                consent_create_kwargs["email_confirmation_requested"] = timezone.now()
            else:
                consent_create_kwargs["email_confirmed"] = True
        except ObjectDoesNotExist:
            create_kwargs = {
                User.EMAIL_FIELD: email,
                "is_active": False,
            }
            if User.EMAIL_FIELD != User.USERNAME_FIELD:
                username = get_random_secret_key()
                while User.objects.filter(**{User.EMAIL_FIELD: username}).exists():
                    username = get_random_secret_key()
                create_kwargs[User.USERNAME_FIELD] = username
            for field_name in [
                f for f in User.REQUIRED_FIELDS if f not in create_kwargs
            ]:
                # Custom auth models have to implement this method if they want
                # to create rows with just an email on-the-fly
                create_kwargs[field_name] = User.get_consent_empty_value(field_name)
            user = get_user_model().objects.create(**create_kwargs)
            user.set_unusable_password()
            user.save()
            if require_confirmation:
                consent_create_kwargs["email_confirmation_requested"] = timezone.now()
        return cls.objects.create(source=source, user=user, **consent_create_kwargs)

    def optout(self, is_everything=False):
        """
        Ensures that user is opted out of this consent.
        """
        return EmailOptOut.objects.get_or_create(
            user=self.user,
            consent=self,
            is_everything=is_everything,
        )[0]

    def confirm(self):
        """
        Marks a consent as confirmed. This will not delete any potential optouts
        already existing.
        """
        self.email_confirmed = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.email_hash and self.user and self.user.email:
            self.email_hash = utils.get_email_hash(self.user.email)
        return super().save(*args, **kwargs)

    def is_valid(self):
        """
        Try to avoid using this - instead, do lookups directly of what you need.
        """
        return self.email_confirmed and not (
            self.optouts.all().exists()
            or self.user.email_optouts.filter(is_everything=True).exists()
        )

    @property
    def email(self):
        return self.user.email

    @property
    def confirm_token(self):
        return utils.get_consent_token(self, salt=consent_settings.CONFIRM_SALT)


class EmailCampaign(models.Model):
    """
    For every type of email that goes out, specify:

    1. a name of the campaign
    2. the type of consent necessary (prefer to use existing consents and don't invent new ones)

    Notice that users don't opt out of a campaign, but they withdraw their
    consent from the original source of when it was given and to which we assume
    we can send the campaign.
    """

    name = models.CharField(max_length=255, verbose_name=_("name"))
    consent = models.ManyToManyField(ConsentSource)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class EmailOptOut(models.Model):
    """
    A user can opt out of different scopes, thus withdrawing their consent:

    * Everything
    * A specific consent

    Notice that for some types of emails, a user may not opt out: For instance,
    if they are members of an association and it calls its members to the
    general assembly.

    Setting ``consent=None`` is the same as opting out of everything.

    Anonymization: If a user is deleted, we still want to be able to store their
    opt-out. While the email is deleted, it may re-occur because of subsequent
    data imports. Therefore, we store a unique hash.
    """

    user = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        related_name="email_optouts",
        on_delete=models.SET_NULL,
    )
    consent = models.ForeignKey(
        "UserConsent",
        blank=True,
        null=True,
        related_name="optouts",
        on_delete=models.SET_NULL,
    )
    is_everything = models.BooleanField(default=False, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    email_hash = models.UUIDField()

    def save(self, *args, **kwargs):
        if self.consent_id is None:
            self.is_everything = True
        if not self.email_hash and self.user and self.user.email:
            self.email_hash = utils.get_email_hash(self.user.email)
        return super().save(*args, **kwargs)
