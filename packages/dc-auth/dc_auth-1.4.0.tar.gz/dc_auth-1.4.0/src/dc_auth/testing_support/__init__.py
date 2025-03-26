"""
Test utilities and functions for dcauth.
"""
from copy import deepcopy

from django.db import transaction
from django.dispatch import receiver
from django.test import RequestFactory
from django_cas_ng.signals import cas_user_authenticated
import pytest

from .factories import SECURE_PASSWORD

GROUP_FORMAT_STRING = 'CN={},OU=Groups,OU=Accounts,DC=ASVO,DC=AAO,DC=GOV,DC=AU'


# pylint: disable=invalid-name,redefined-outer-name
@pytest.fixture
def profile_factory(db):
    """
    Pytest fixture to get a `ProfileFactory`
    """
    # pylint: disable=import-outside-toplevel,unused-argument
    from .factories.user import ProfileFactory

    return ProfileFactory


@pytest.fixture
def user_factory(db):
    """
    Pytest fixture to get a `UserFactory`
    """
    # pylint: disable=import-outside-toplevel,unused-argument
    from .factories.user import UserFactory

    return UserFactory


@pytest.fixture
def profile(profile_factory):
    """
    Pytest fixture to get a valid `Profile` object.
    """
    p = profile_factory.create()
    p.ensure_profile_email_exists_and_valid()
    return p


@pytest.fixture
def user(profile):
    """
    Pytest fixture to get a valid `User` object.
    """
    return profile.user


@pytest.fixture
def affiliation(faker):
    """
    Pytest fixture for a dummy affiliation.
    """
    return faker.company()


@pytest.fixture
def secure_password():
    """
    Pytest fixture for a dummy but known and accepted password.
    """
    return SECURE_PASSWORD


def add_mock_verification(
    *, username=None, user_attrs=None, monkeypatch, user=None, **kwargs
):
    """
    Helper function to mock out CAS verify_ticket method to override
    requests/responses from CAS for the purposes of testing.
    """
    if user is None and username is None:
        raise ValueError("Either a user or a username must be provided")
    if username is None:
        username = user.username
    if user_attrs is None:
        if user is None:
            user_attrs = {}
        else:
            user_attrs = create_cas_attrs_from_user(user, **kwargs)

    def mock_verify(self, ticket):
        """Mock verification"""
        # pylint: disable=unused-argument
        attrs = deepcopy(user_attrs)
        attrs.update({'ticket': ticket, 'service': 'service_url'})
        proxy_ticket = None
        return username, attrs, proxy_ticket

    # we mock out the verify method so that we can bypass the external http
    # calls needed for real authentication since we are testing the logic
    # around authentication.
    monkeypatch.setattr('cas.CASClientV2.verify_ticket', mock_verify)
    return {"ticket": 'fake-ticket', "service": 'fake-service'}


def mock_login_cas(monkeypatch, django_user_model, username, user_attrs):
    """
    Helper function to mock out CAS login.
    """
    # pylint: disable=import-outside-toplevel
    from django_cas_ng.backends import CASBackend

    factory = RequestFactory()
    request = factory.get('/login/')
    request.session = {}

    callback_values = {}

    @receiver(cas_user_authenticated)
    def callback(sender, **kwargs):
        # pylint: disable=unused-argument
        callback_values.update(kwargs)

    auth_kwargs = add_mock_verification(
        username=username, user_attrs=user_attrs, monkeypatch=monkeypatch
    )

    # sanity check
    with transaction.atomic():
        assert not django_user_model.objects.filter(
            username=username,
        ).exists()

    with transaction.atomic():
        backend = CASBackend()
        auth_user = backend.authenticate(request=request, **auth_kwargs)

    assert auth_user is not None

    return callback_values, auth_user, request


def create_cas_attrs_from_user(
    user, override=None, group_format_string=GROUP_FORMAT_STRING,
):
    """
    Give a similar-enough dictionary of attributes from a CAS response. The
    response can be overridden/expanded by `override`.
    """
    try:
        groups = [
            group_format_string.format(group.name)
            for group in user.groups.all()
        ]
    except ValueError:
        groups = []

    attrs = {
        'isFromNewLogin': 'false',
        'authenticationDate': '2019-03-07T23:17:23.351Z[UTC]',
        'displayName': f'{user.first_name} {user.last_name}',
        'successfulAuthenticationHandlers': 'Active Directory',
        'groups': groups,
        'orcid': user.profile.orcid,
        'affiliation': user.profile.affiliation,
        'credentialType': 'UsernamePasswordCredential',
        'authenticationMethod': 'Active Directory',
        'longTermAuthenticationRequestTokenUsed': 'false',
        'last_name': user.last_name,
        'first_name': user.first_name,
        'email': user.email,
        'additional_emails': [
            e.address for e in user.profile.emails.filter(confirmed=True)
        ],
        'is_dc_auth_test_login': True,
    }

    if override is not None:
        attrs.update(override)

    return attrs
