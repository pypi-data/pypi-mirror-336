"""
Djangorestframework specific support for Data Central
"""
import logging

from rest_framework.authentication import BaseAuthentication

from ..backends import (
    get_access_token_from_request, get_cached_user_from_access_token,
)

logger = logging.getLogger(__name__)


class OAuth2ResourceAuthentication(BaseAuthentication):
    """
    djangorestframework authentication class which handles OAuth 2 resource
    server authentication.
    """
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of
        (user, auth_context).
        """
        logging.info(
            "Checking OAuth2ResourceAuthentication with request %s",
            request
        )
        access_token = get_access_token_from_request(request)

        # We're currently giving no context, but we may wish to down the line
        user = get_cached_user_from_access_token(access_token)
        if user:
            return (user, None)
        return None
