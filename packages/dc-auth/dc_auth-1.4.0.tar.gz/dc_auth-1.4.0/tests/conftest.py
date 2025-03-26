from urllib.parse import urlencode
from secrets import token_hex

import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def oauth_authorisation_server(httpserver, settings):
    access_token = token_hex()
    client_id = token_hex()
    client_secret = token_hex()
    # Profile endpoint
    httpserver.expect_request(
        "/profile",
        method="GET",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    ).respond_with_json({
        "id": "casuser",
        "attributes": {
            "mail": "casuser@example.org",
            "givenName": "CAS",
            "sn": "User",
            "affiliation": "test",
        },
        "something": "else",
    })

    # Introspection endpoint
    httpserver.expect_request(
        "/introspection",
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=urlencode({
            "token": access_token,
            "token_type_hint": "access_token",
        })
    ).respond_with_json({
        "active": True,
        "client_id": "l2345678",
        "username": "jdoe",
        "scope": "read write manage",
        "sub": "Z5O3upPC88QrAjx00dis",
        "aud": "https://protected.example.net/resource",
        "iss": "https://cas.example.com/oidc",
        "exp": 1419356238,
        "iat": 1419350238,
    })

    settings.DC_OAUTH2_INTROPECTION_URL = httpserver.url_for("/introspection")
    settings.DC_OAUTH2_PROFILE_URL = httpserver.url_for("/profile")
    settings.DC_OAUTH2_RESOURCE_CLIENT_ID = client_id
    settings.DC_OAUTH2_RESOURCE_CLIENT_SECRET = client_secret

    return {
        "httpserver": httpserver,
        "access_token": access_token,
    }


@pytest.fixture
def api_rf():
    return APIRequestFactory()

@pytest.fixture
def dummy_drf_view():
    from rest_framework.views import APIView

    class DummyView(APIView):
        ...

    return DummyView()
