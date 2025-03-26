"""
Additional models used for authentication and authorisation in Data Central.

The user model comes from Django.
"""
import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# User model extended as per
# https://web.archive.org/web/20220204223759/https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone


class Profile(models.Model):
    """
    Additional profile information required about users that is not stored in
    the Django user model.

    Currently this is the ORCID and the affiliation of the user, as well as
    referencing the additional emails a user may have.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    email_confirmed = models.BooleanField(default=False)

    # extra fields to populate from LDAP/AD
    affiliation = models.CharField(max_length=255, blank=False)
    orcid = models.CharField(
        max_length=100, blank=False, null=False, default="-"
    )

    def ensure_profile_email_exists_and_valid(self):
        """
        Ensure that the profile email for the address stored on the user model
        exists, so that users can change which email is their primary email.
        """
        user_email = self.user.email

        if not self.email_confirmed:
            logger.warning(
                "Email %s unconfirmed for %s, still checking for duplicates",
                user_email, self.user.username
            )

            # For unconfirmed emails, this should be 0
            if ProfileEmail.objects.filter(address=user_email).count():
                raise RuntimeError(f"Duplicate unconfirmed email {user_email}")

        elif not self.user.is_active:
            # Email confirmed but user inactive
            # We're not going to touch LDAP here, only raise an appropriate
            # error
            if ProfileEmail.objects.filter(address=user_email).count():
                raise RuntimeError(
                    f"Duplicate confirmed email {user_email} for inactive "
                    "account"
                )
            raise RuntimeError(
                f"Confirmed email {user_email} for inactive account"
            )
        else:
            if ProfileEmail.objects.filter(address=user_email).count():
                if user_email not in {e.address for e in self.emails.all()}:
                    raise RuntimeError(
                        f"Email {user_email} associated with multiple users"
                    )

            else:
                profile_email = ProfileEmail(
                    profile=self, address=user_email, confirmed=True,
                )
                profile_email.save()

    def get_team_names(self):
        """
        Return team names based on groups user is in, with a blacklist to
        filter out non-teams.

        This should *not* be used for permission handling, and may be out of
        date. If you need an accurate list of the user's teams, then you will
        need to use dcteams/dcldap.
        """
        teams = set()
        for group in self.user.groups.all():
            team_name = group.name.split('-', maxsplit=2)[0]
            if team_name not in settings.DC_USER_TEAM_BLACKLIST_FILTER:
                teams.add(team_name)

        return teams


# auto-create the profile associated with this user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_django_user_profile(sender, instance, created, **kwargs):
    """
    A new django_user has been created, ensure a profile object has been too.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # if the user has just been created, ensure the django profile has been too
    logger.debug(
        "User saved signal received: %s, %s, %s, %s",
        sender, instance, created, kwargs,
    )
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


class ProfileEmail(models.Model):
    """
    Model to allow users to have multiple email addresses.

    If read from LDAP, the email is assumed to be confirmed, and will be set to
    true, otherwise will default to false (and will need to be confirmed in
    accounts).
    """
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="emails",
    )
    address = models.EmailField(
        unique=True, blank=False, null=False, editable=False,
    )
    confirmed = models.BooleanField(default=False)
