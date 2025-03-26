"""
Django signals handlers for dcauth.

As django-cas-ng uses a signal to populate additional parts of the user model,
the required receiver is implemented in this module.
"""
import logging

from django.apps import apps
from django.dispatch import receiver, Signal
from django_cas_ng.signals import cas_user_authenticated

from .backends import (
    ensure_profile_for_user, ensure_profile_emails_for_user,
    ensure_groups_for_user,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
cas_user_set_up = Signal()


@receiver(cas_user_authenticated)
def populate_user_model(
    *, user, created, attributes, ticket, service, request, **kwargs
):
    """
    Create the user profile if it hasn't been already, populate orcid,
    get_or_create all groups returned and associate with this user.

    The structure of attributes will be something similar to::

        {
            'isFromNewLogin': 'true',
            'authenticationDate': '2019-03-07T23:17:23.351Z[UTC]',
            'displayName': 'Elizabeth Mannering',
            'successfulAuthenticationHandlers': 'Active Directory',
            'groups': [
                'CN=Testing,OU=Groups,OU=Accounts,DC=ASVO,DC=AAO,DC=GOV,DC=AU',
            ],
            'orcid': '-',
            'credentialType': 'UsernamePasswordCredential',
            'authenticationMethod': 'Active Directory',
            'longTermAuthenticationRequestTokenUsed': 'false',
            'last_name': 'Mannering',
            'first_name': 'Elizabeth',
            'email': 'Liz.Mannering@mq.edu.au'
        }

    """
    logger.debug(
        "CAS signal called with user %s; created %s; attributes %s ; "
        "ticket %s; service %s; request %s; kwargs %s",
        user, created, attributes, ticket, service, request, kwargs,
    )
    if user:
        try:
            # - - - - - - - - - - - Profile - - - - - - - - - - -

            orcid = attributes.get("orcid")
            affiliation = attributes.get("affiliation")
            ensure_profile_for_user(
                user=user, orcid=orcid, affiliation=affiliation,
            )

            # - - - - - - - - - - - Emails - - - - - - - - - - -
            additional_emails = attributes.get("additional_emails", [])
            ensure_profile_emails_for_user(
                user=user, additional_emails=additional_emails,
            )

            # - - - - - - - - - - - Groups - - - - - - - - - - -

            groups = attributes.get("groups", None)
            ensure_groups_for_user(user=user, groups=groups)

            # - - - - - - - - - - - User - - - - - - - - - - - -
            # ensure passwords are never stored locally
            user.set_unusable_password()
            user.save()

        except Exception:
            logger.exception(
                "Could not populate user from CAS response "
                "(could be missing attributes): %s",
                attributes,
            )

        results = cas_user_set_up.send_robust(
            apps.get_model(app_label="dc_auth", model_name="profile"),
            user=user,
        )
        for req, resp in results:
            if isinstance(resp, Exception):
                logger.error(resp)
