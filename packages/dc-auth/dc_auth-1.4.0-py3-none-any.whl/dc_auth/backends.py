"""
Data Central Authentication backends for django
"""
import logging

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.db.models import Q
import requests

from .models import ProfileEmail

logger = logging.getLogger(__name__)
UserModel = get_user_model()
CACHE_PREFIX = "DCOAUTH"


class BearerAuth(requests.auth.AuthBase):
    """
    Helper class for requests which handles adding in an access_token to a
    request correctly.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, *, access_token):
        self.token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer {self.token}"
        return r


def get_or_create_user(*, username, first_name, last_name, email):
    """
    Get or create a user based on their username, updating their first name,
    last name and email if needed.

    This is only needed for the OAuth 2 authentication backend, as the CAS
    backend performs this internally.
    """
    # We always want to update the values, so use the defaults=create_defaults
    # fallback
    user, created = UserModel.objects.update_or_create(
        defaults={
            "first_name": first_name, "last_name": last_name, "email": email,
        },
        username=username,
    )

    # ensure passwords are never stored locally
    user.set_unusable_password()
    logger.debug(
        "User %s %s", user.username, "created" if created else "updated",
    )

    return user


def ensure_profile_for_user(*, user, orcid, affiliation):
    """
    Ensure that `user` has an associated profile, and update said profile with
    the provided `orcid` and `affiliation`.
    """
    if orcid is None:
        orcid = "-"
    # ensure the profile object exists
    if not hasattr(user, "profile"):
        apps.get_model(
            app_label="dc_auth", model_name="profile"
        ).objects.create(user=user)
        user.profile.save()

    # custom attributes
    user.profile.orcid = orcid
    user.profile.affiliation = affiliation

    # if user is authenticated with CAS, their email confirmation state
    # must be true as users are only pushed to ldap after email
    # confirmation
    user.profile.email_confirmed = True
    user.profile.save()
    return user.profile


def ensure_profile_emails_for_user(*, user, additional_emails):
    """
    Ensure that `user.profile.emails` matches that given in additional_emails.

    Does not remove unconfirmed emails, so that users can confirm their emails
    after having logged in again.
    """
    if additional_emails:
        if isinstance(additional_emails, str):
            additional_emails = [additional_emails]
        # Clear out old emails
        user.profile.emails.filter(
            ~Q(address__in=additional_emails),
            confirmed=True,
        ).delete()
        for email in additional_emails:
            ProfileEmail.objects.update_or_create(
                defaults={"confirmed": True},
                create_defaults={"confirmed": True},
                profile=user.profile,
                address=email,
            )
    else:
        # Remove all additional emails
        user.profile.emails.all().delete()
    user.profile.ensure_profile_email_exists_and_valid()


def ensure_groups_for_user(*, user, groups):
    """
    Ensure that the groups for a user match that contained in LDAP.

    This also ensures that users in the specified groups are given the correct
    django roles.
    """
    # clear any initial groups, then add back the ones in ldap
    user.groups.clear()
    if groups:
        if isinstance(groups, str):
            groups = [groups]
        for group_attr in groups:
            group_name = group_attr.split("CN=")[1].split(",")[0]

            group, created = apps.get_model(
                app_label="auth", model_name="group"
            ).objects.get_or_create(name=group_name)

            group.user_set.add(user)
            if created:
                logger.info("Created %s", group_name)
            logger.info("Added %s to %s", user.username, group_name)

    # make user staff if in group dc-admin
    if user.groups.filter(name="dc-admin").exists():
        user.is_staff = True
        logger.info("Made %s staff", user.username)
        user.save()


def is_oauth2_access_token_valid(
    *, token, introspection_url=None, auth=None,
):
    """
    Asks CAS (or the authentication provider) if the provided access token is
    valid.
    """
    if introspection_url is None:
        introspection_url = settings.DC_OAUTH2_INTROPECTION_URL
    if auth is None:
        # CAS requires that this is done via basic auth
        auth = (
            settings.DC_OAUTH2_RESOURCE_CLIENT_ID,
            settings.DC_OAUTH2_RESOURCE_CLIENT_SECRET
        )

    resp = requests.post(
        introspection_url,
        data={"token": token, "token_type_hint": "access_token"},
        timeout=settings.DC_OAUTH2_REQUEST_TIMEOUT,
        auth=auth,
    )
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.exception("Failed to check token validity")
        return None

    validation_response = resp.json()
    if validation_response.get("active"):
        return True
    return False


def get_access_token_from_request(request):
    """
    Extract the access token from the django request object.
    """
    auth_header = request.headers.get("Authorization", "").strip()
    if not auth_header.startswith("Bearer"):
        return None
    token = auth_header.split(" ")[1]
    return token


def get_or_create_oauth2_user_profile(
    *, token, profile_url=None,
):
    """
    Using CAS (or the provided authentication server) profile endpoint, create
    the user and profile, or update them with the latest values.
    """
    if profile_url is None:
        profile_url = settings.DC_OAUTH2_PROFILE_URL
    resp = requests.get(
        profile_url,
        auth=BearerAuth(access_token=token),
        timeout=settings.DC_OAUTH2_REQUEST_TIMEOUT,
    )
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    profile_response = resp.json()

    # This is always in the top level document
    username = profile_response["id"]

    # Extract out where the rest of the profile information is
    if "attributes" in profile_response:
        attributes = profile_response["attributes"]
    else:
        attributes = profile_response

    try:
        user = get_or_create_user(
            username=username,
            first_name=attributes["givenName"],
            last_name=attributes["sn"],
            email=attributes["mail"],
        )
    except KeyError:
        logger.exception(
            "OAuth2 Profile response missing user details: %s",
            profile_response
        )
        return None

    ensure_profile_for_user(
        user=user,
        affiliation=attributes.get("affiliation"),
        orcid=attributes.get("orcid")
    )
    ensure_profile_emails_for_user(
        user=user,
        additional_emails=attributes.get("additional_emails"),
    )
    ensure_groups_for_user(
        user=user,
        groups=attributes.get("groups", None),
    )

    return user


def get_cached_user_from_access_token(token):
    """
    This checks if `token` is valid, and returns the user associated with the
    token.

    To reduce the number of calls to the profile endpoint, the user's details
    are only updated if the token is not in the cache (which is by default 5
    minutes, see `settings.DC_OAUTH2_CACHE_TIME`).
    """
    if token is None:
        logging.error("No token provided")
        return None
    if is_oauth2_access_token_valid(token=token):
        logging.debug("Valid token sent")
        username = cache.get(CACHE_PREFIX + token)
        if username is not None:
            try:
                return UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                logger.warning(
                    "Previously OAuth2 logged in user %s no longer has "
                    "user stored in db",
                    username
                )
                # We will fall through to the other path and get the user's
                # profile
        user = get_or_create_oauth2_user_profile(token=token)
        cache.set(
            CACHE_PREFIX + token,
            user.username,
            settings.DC_OAUTH2_CACHE_TIME,
        )
        return user
    logging.error("Invalid token %s sent", token)
    return None


class OAuth2ResourceBackend(ModelBackend):
    """
    A OAuth 2.x resource server backend for Data Central CAS.

    Uses the existing user model support that the ModelBackend provides, and
    simply overrides the `authenticate` method to handle token checking and
    user creation.
    """
    # pylint: disable=arguments-differ
    def authenticate(self, request, *, access_token=None):
        """
        Authentication method required for backend.

        This allows either request or access_token to be `None`, but not both.
        """
        logging.info(
            "Checking OAuth2ResourceBackend with request %s access_token %s",
            request, access_token,
        )
        if request is None and access_token is None:
            logging.error("Unable to authenticate with OAuth2ResourceBackend")
            return None
        if access_token is None:
            access_token = get_access_token_from_request(request)
        return get_cached_user_from_access_token(access_token)
