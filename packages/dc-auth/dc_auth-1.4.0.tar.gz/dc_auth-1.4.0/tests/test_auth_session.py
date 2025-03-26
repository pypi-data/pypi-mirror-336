from secrets import token_hex

import pytest

from django.apps import apps
from django.contrib.auth import authenticate
from django.urls import reverse

from dc_auth.testing_support import (
    mock_login_cas, add_mock_verification, create_cas_attrs_from_user,
)
from dc_auth.testing_support.factories.user import UserFactory

LOGIN_URL = reverse('cas_ng_login')


@pytest.mark.django_db
def test_signal_when_user_is_created(monkeypatch, django_user_model):
    """
    Test basic login for cas user.

    Note. This user does not exist in ldap. CAS verification on client is
    mocked.
    """
    # using a fixture would auto-add user to the db, which do not want
    user = UserFactory()

    user_attrs = {
        'affiliation': user.profile.affiliation,
        'orcid': user.profile.orcid,
    }

    callback_values, auth_user, request = mock_login_cas(
        monkeypatch, django_user_model, user.username, user_attrs,
    )

    assert 'user' in callback_values
    assert callback_values.get('user') == auth_user
    assert callback_values.get('created')
    assert 'attributes' in callback_values
    for key, val in user_attrs.items():
        assert callback_values['attributes'][key] == val
    assert 'ticket' in callback_values
    assert callback_values['ticket'] == 'fake-ticket'
    assert 'service' in callback_values
    assert callback_values['service'] == 'fake-service'

    # ensure user is created in db
    django_user = django_user_model.objects.get(username=user.username)
    assert django_user.profile.affiliation == user.profile.affiliation
    assert django_user.profile.orcid == user.profile.orcid


@pytest.mark.django_db
def test_signal_user_created_with_groups(monkeypatch, django_user_model):
    """
    Test login for cas user with groups.

    Note. This user does not exist in ldap. CAS verification on client is
    mocked.
    """
    # using a fixture would auto-add user to the db, which do not want
    user = UserFactory()

    user_attrs = {
        'affiliation': user.profile.affiliation,
        'orcid': user.profile.orcid,
        'groups': [
            'CN=DEVILS,OU=Groups,OU=Accounts,DC=ASVO,DC=AAO,DC=GOV,DC=AU',
        ]
    }

    callback_values, auth_user, request = mock_login_cas(
        monkeypatch, django_user_model, user.username, user_attrs,
    )

    assert 'user' in callback_values
    assert callback_values.get('user') == auth_user
    assert callback_values.get('created')
    assert 'attributes' in callback_values
    for key, val in user_attrs.items():
        assert callback_values['attributes'][key] == val
    assert 'ticket' in callback_values
    assert callback_values['ticket'] == 'fake-ticket'
    assert 'service' in callback_values
    assert callback_values['service'] == 'fake-service'

    # ensure user is created in db
    django_user = django_user_model.objects.get(username=user.username)
    user_groups = django_user.groups.all()
    assert len(user_groups) == 1
    assert user_groups[0].name == "DEVILS"


@pytest.mark.django_db
def test_signal_user_created_with_admin_group(monkeypatch, django_user_model):
    """
    Test login for cas user with groups.

    Note. This user does not exist in ldap. CAS verification on client is
    mocked.
    """
    # using a fixture would auto-add user to the db, which do not want
    user = UserFactory()

    user_attrs = {
        'affiliation': user.profile.affiliation,
        'orcid': user.profile.orcid,
        'groups': [
            'CN=dc-admin,OU=Groups,OU=Accounts,DC=ASVO,DC=AAO,DC=GOV,DC=AU',
        ]
    }

    callback_values, auth_user, request = mock_login_cas(
        monkeypatch, django_user_model, user.username, user_attrs,
    )

    assert 'user' in callback_values
    assert callback_values.get('user') == auth_user
    assert callback_values.get('created')
    assert 'attributes' in callback_values
    for key, val in user_attrs.items():
        assert callback_values['attributes'][key] == val
    assert 'ticket' in callback_values
    assert callback_values['ticket'] == 'fake-ticket'
    assert 'service' in callback_values
    assert callback_values['service'] == 'fake-service'

    # ensure user is created in db
    django_user = django_user_model.objects.get(username=user.username)
    user_groups = django_user.groups.all()
    assert len(user_groups) == 1
    assert user_groups[0].name == "dc-admin"
    assert django_user.is_staff


@pytest.mark.django_db
def test_login_authenticate_and_create_user(
    monkeypatch, django_user_model, settings, client
):
    """
    Test the consequence of the dc_auth handler for cas_user_authenticated
    i.e., has_unusable_password=True, email_confirmed=True etc
    Handle missing orcid

    Note. This user does not exist in ldap. CAS verification on client is mocked.
    """
    # using a fixture would auto-add user to the db, which do not want
    user = UserFactory()

    # No need to test the message framework
    settings.CAS_LOGIN_MSG = None
    # Make sure we use our backend
    settings.AUTHENTICATION_BACKENDS = ['django_cas_ng.backends.CASBackend']

    auth_kwargs = add_mock_verification(
        username=user.username,
        user_attrs={'affiliation': user.profile.affiliation},
        monkeypatch=monkeypatch,
    )

    response = client.get(LOGIN_URL, auth_kwargs, follow=False)

    assert response.status_code == 302
    assert response['Location'] == '/'
    django_user = django_user_model.objects.get(username=user.username)
    assert django_user.is_authenticated is True
    assert django_user.profile.affiliation == user.profile.affiliation
    assert django_user.profile.email_confirmed is True
    assert django_user.is_active is True
    assert django_user.has_usable_password() is False
    assert django_user.profile.orcid == '-'


@pytest.mark.django_db
def test_mock_verification_user_only(
    monkeypatch, django_user_model, settings, user, client
):
    """
    This checks that the details are read from the user correctly as part of
    add_mock_verification.
    """
    # No need to test the message framework
    settings.CAS_LOGIN_MSG = None
    # Make sure we use our backend
    settings.AUTHENTICATION_BACKENDS = ['django_cas_ng.backends.CASBackend']

    old_username = user.username
    affiliation = user.profile.affiliation
    orcid = user.profile.orcid

    auth_kwargs = add_mock_verification(user=user, monkeypatch=monkeypatch)

    user.delete()

    response = client.get(LOGIN_URL, auth_kwargs, follow=False)

    assert response.status_code == 302
    assert response['Location'] == '/'
    django_user = django_user_model.objects.get(username=old_username)
    assert django_user.is_authenticated is True
    assert django_user.profile.affiliation == affiliation
    assert django_user.profile.email_confirmed is True
    assert django_user.is_active is True
    assert django_user.has_usable_password() is False
    assert django_user.profile.orcid == orcid


@pytest.mark.django_db
def test_login_group_removal(
    monkeypatch, django_user_model, settings, user, client,
):
    """
    Test the consequence of the dc_auth handler for cas_user_authenticated
    i.e., has_unusable_password=True, email_confirmed=True etc
    Handle missing orcid

    Note. This user does not exist in ldap. CAS verification on client is mocked.
    """
    # If user not active, login fails
    user.is_active = True
    user.save()

    group_name = "testgroup"
    group_model = apps.get_model(app_label='auth', model_name="group")
    group, created = group_model.objects.get_or_create(name=group_name)
    group.user_set.add(user)

    auth_kwargs = add_mock_verification(
        username=user.username,
        user_attrs={'affiliation': user.profile.affiliation},
        monkeypatch=monkeypatch,
    )

    response = client.get(LOGIN_URL, auth_kwargs, follow=False)
    assert response.status_code == 302
    assert response['Location'] == '/'

    django_user = django_user_model.objects.get(username=user.username)
    user_groups = django_user.groups.all()
    assert len(user_groups) == 0


@pytest.mark.django_db
def test_basic_oauth2_flow(oauth_authorisation_server, rf, settings):
    settings.AUTHENTICATION_BACKENDS = [
        'dc_auth.backends.OAuth2ResourceBackend'
    ]
    httpserver = oauth_authorisation_server["httpserver"]
    access_token = oauth_authorisation_server["access_token"]
    request = rf.get(
        "/",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    user = authenticate(request=request)
    assert user is not None


@pytest.mark.django_db
def test_oauth2_flow_no_request(oauth_authorisation_server, settings):
    settings.AUTHENTICATION_BACKENDS = [
        'dc_auth.backends.OAuth2ResourceBackend'
    ]
    httpserver = oauth_authorisation_server["httpserver"]
    access_token = oauth_authorisation_server["access_token"]
    user = authenticate(access_token=access_token)
    assert user is not None


@pytest.mark.django_db
def test_oauth2_flow_no_request_no_token(oauth_authorisation_server, settings):
    settings.AUTHENTICATION_BACKENDS = [
        'dc_auth.backends.OAuth2ResourceBackend'
    ]
    httpserver = oauth_authorisation_server["httpserver"]
    access_token = oauth_authorisation_server["access_token"]
    user = authenticate(access_token=None)
    assert user is None


@pytest.mark.django_db
def test_oauth2_flow_missing_token(oauth_authorisation_server, rf, settings):
    settings.AUTHENTICATION_BACKENDS = [
        'dc_auth.backends.OAuth2ResourceBackend'
    ]
    httpserver = oauth_authorisation_server["httpserver"]
    access_token = oauth_authorisation_server["access_token"]
    request = rf.get("/")
    user = authenticate(request=request)
    assert user is None


@pytest.mark.django_db
def test_oauth2_flow_wrong_token(oauth_authorisation_server, rf, settings):
    settings.AUTHENTICATION_BACKENDS = [
        'dc_auth.backends.OAuth2ResourceBackend'
    ]
    httpserver = oauth_authorisation_server["httpserver"]
    access_token = token_hex()
    request = rf.get(
        "/",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    user = authenticate(request=request)
    assert user is None


@pytest.mark.django_db
def test_oauth2_flow_drf(
    oauth_authorisation_server, api_rf, settings, dummy_drf_view
):
    settings.REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'dc_auth.drf_support.OAuth2ResourceAuthentication',
        ]
    }

    httpserver = oauth_authorisation_server["httpserver"]
    access_token = oauth_authorisation_server["access_token"]
    request = api_rf.get(
        "/",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    drf_request = dummy_drf_view.initialize_request(request)

    assert drf_request.user is not None
