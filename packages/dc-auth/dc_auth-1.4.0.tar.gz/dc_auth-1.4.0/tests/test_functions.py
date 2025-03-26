import pytest

from hypothesis import given, example, settings as hy_settings, HealthCheck
from hypothesis.strategies import text

from django.apps import apps
from django.conf import settings


@given(group_name=text())
@hy_settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@example(group_name="dc")
@example(group_name="dc-admin")
@example(group_name="asvo-admin")
@pytest.mark.django_db
def test_get_team_names(group_name, user_factory):
    # This is so we get a new user per hypothesis run
    user = user_factory.create()

    # test user has no teams
    assert not user.profile.get_team_names()

    group, created = apps.get_model(
        app_label="auth", model_name="group"
    ).objects.get_or_create(name=group_name)

    is_blacklisted = False
    for bl_prefix in settings.DC_USER_TEAM_BLACKLIST_FILTER:
        if group_name.startswith(bl_prefix):
            is_blacklisted = True
            break

    group.user_set.add(user)

    if is_blacklisted:
        assert not user.profile.get_team_names()
    else:
        assert user.profile.get_team_names()
