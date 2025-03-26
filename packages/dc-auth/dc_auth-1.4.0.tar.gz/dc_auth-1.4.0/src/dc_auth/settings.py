"""
Settings to connect to the DC CAS server
"""
import os
import re

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Shared django settings
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Login Urls
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

LOGIN_URL = reverse_lazy("cas_ng_login")
LOGIN_REDIRECT_URL = reverse_lazy("index")
LOGOUT_REDIRECT_URL = reverse_lazy("index")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Auth config
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

AUTHENTICATION_BACKENDS = (
    "django_cas_ng.backends.CASBackend",
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           CAS config
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

CAS_SERVER_URL = "https://auth-mfa.datacentral.org.au/cas/"
DEVELOPMENT_CAS_SERVER_URL = " https://dev-mfa.datacentral.org.au/cas/"
CAS_CREATE_USER = True

# Where to send a user after logging in or out if there is no referrer and no
# next page set
CAS_REDIRECT_URL = "/"

# when logging out of the application, always redirect to CAS_REDIRECT_URL
CAS_IGNORE_REFERER = True

# If True any attributes returned by the CAS provider included in the ticket
# will be applied to the User model returned by authentication.
# This is useful if your provider is including details about the User which
# should be reflected in your model
CAS_APPLY_ATTRIBUTES_TO_USER = True

# a dict used to rename the (key of the) attributes that the CAS server may
# return
CAS_RENAME_ATTRIBUTES = {
    "sn": "last_name",
    "givenName": "first_name",
    "mail": "email",
    "otherMailbox": "additional_emails",
}

CAS_VERSION = "3"

# CAS defaults, here in case they do not get set
# (e.g. due to monkeypatching CAS login)
CAS_ADMIN_REDIRECT = True
CAS_ADMIN_PREFIX = None
CAS_CHECK_NEXT = True
CAS_CREATE_USER_WITH_ID = False
CAS_EXTRA_LOGIN_PARAMS = None
CAS_FORCE_CHANGE_USERNAME_CASE = None
CAS_FORCE_SSL_SERVICE_URL = False
CAS_LOCAL_NAME_FIELD = None
CAS_LOGGED_MSG = gettext_lazy("You are logged in as %s.")
CAS_LOGIN_MSG = gettext_lazy("Login succeeded. Welcome, %s.")
CAS_LOGIN_URL_NAME = 'cas_ng_login'
CAS_LOGOUT_COMPLETELY = True
CAS_LOGOUT_URL_NAME = 'cas_ng_logout'
CAS_PROXY_CALLBACK = None
CAS_RENEW = False
CAS_RETRY_LOGIN = False
CAS_SESSION_FACTORY = None
CAS_STORE_NEXT = False
CAS_USERNAME_ATTRIBUTE = 'cas:user'
CAS_VERIFY_SSL_CERTIFICATE = True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                   OAuth 2 resource server config
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DC_OAUTH2_CACHE_TIME = 5 * 60  # 5 minutes in seconds
DC_OAUTH2_BASE_URL = CAS_SERVER_URL + "oauth2.0/"
DC_OAUTH2_INTROPECTION_URL = DC_OAUTH2_BASE_URL + "introspect"
DC_OAUTH2_PROFILE_URL = DC_OAUTH2_BASE_URL + "profile"
DC_OAUTH2_REQUEST_TIMEOUT = 5

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                   OIDC resource server config
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DC_OIDC_BASE_URL = CAS_SERVER_URL + "oidc/"
DC_OIDC_DISCOVERY_URL = DC_OIDC_BASE_URL + ".well-known/openid-configuration"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Service URLS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DC_STATIC_URL_FALLBACK = "https://static.datacentral.org.au/dist/"
DC_STATIC_URL = os.environ.get("DC_STATIC_URL", DC_STATIC_URL_FALLBACK)
DC_API_URL = "https://datacentral.org.au"
DC_CMS_URL = "https://docs.datacentral.org.au"
DC_CLOUD_URL = "https://cloud.datacentral.org.au"
DC_WIKI_URL = "https://datacentral.org.au/wiki"
DC_ACCOUNTS_URL = "https://accounts.datacentral.org.au"
DC_TEAMS_URL = "https://teams.datacentral.org.au"
DC_LENS_URL = "https://lens.datacentral.org.au"
DC_REPORTS_URL = "https://reports.datacentral.org.au"
DAS_URL = "https://das.datacentral.org.au"
DC_ARCHIVES_URL = "https://archives.datacentral.org.au"
HTS_URL = "https://hts.datacentral.org.au"
DC_DESKTOPS_URL = "https://desktops.datacentral.org.au"
DC_APPS_URL = "https://apps.datacentral.org.au"
DC_SPECEXPLORE_URL = "https://spectra.datacentral.org.au"
# update link to new jira link to fix the dead link error
DC_SERVICE_DESK_HOME_URL = (
    "https://aaomq.atlassian.net/servicedesk/customer/portal/8"
)
DC_SERVICE_DESK_BUG_URL = DC_SERVICE_DESK_HOME_URL + (
    "/group/24/create/101"
)
DC_SERVICE_DESK_FEATURE_URL = DC_SERVICE_DESK_HOME_URL + (
    "/group/24/create/102"
)
DC_AAT_ARCHIVE_URL = "https://datacentral.org.au/archives/aat/"
DC_MALIN_IMAGES_URL = "https://images.datacentral.org.au/"
DC_TAP_SERVICE_URL = DC_API_URL + "/vo/tap"
DC_API_ENDPOINT_URL = DC_API_URL + "/api/"
DC_VO_DOCS_URL = DC_CMS_URL + "/reference/services/vo/"
DC_ABOUT_URL = DC_API_URL + "/about/"
DC_TIMELINE_URL = DC_CMS_URL + "/timeline/"
DC_BLOG_URL = DC_CMS_URL + "/blog/"
DC_ACKNOWLEDGING_URL = DC_CMS_URL + "/reference/acknowledgements/"
DC_PRIVACY_URL = DC_CMS_URL + "/governance/policies/privacy/"
# update link to new jira link to fix the dead link error
AAT_HELP_DESK_URL = "https://aaomq.atlassian.net/servicedesk/customer/portal/4"
ESO_HELP_DESK_URL = "https://aaomq.atlassian.net/servicedesk/customer/portal/6"

SETTINGS_EXPORT = [
    "DC_STATIC_URL",
    "DC_API_URL",
    "DC_CMS_URL",
    "DC_CLOUD_URL",
    "DC_WIKI_URL",
    "DC_ACCOUNTS_URL",
    "DC_TEAMS_URL",
    "DC_LENS_URL",
    "DC_REPORTS_URL",
    "DAS_URL",
    "DC_ARCHIVES_URL",
    "HTS_URL",
    "DC_DESKTOPS_URL",
    "DC_APPS_URL",
    "DC_SPECEXPLORE_URL",
    "DC_SERVICE_DESK_HOME_URL",
    "DC_SERVICE_DESK_BUG_URL",
    "DC_SERVICE_DESK_FEATURE_URL",
    "DC_AAT_ARCHIVE_URL",
    "DC_MALIN_IMAGES_URL",
    "DC_TAP_SERVICE_URL",
    "DC_API_ENDPOINT_URL",
    "DC_VO_DOCS_URL",
    "DC_ABOUT_URL",
    "DC_TIMELINE_URL",
    "DC_BLOG_URL",
    "DC_ACKNOWLEDGING_URL",
    "DC_PRIVACY_URL",
    "AAT_HELP_DESK_URL",
    "ESO_HELP_DESK_URL",
]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Email
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

EMAIL_HOST = "comms.aao.gov.au"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "noreply@datacentral.org.au"
CONTACT_EMAIL = "contact@datacentral.org.au"
BUG_REPORT_EMAIL = "bug-report@datacentral.org.au"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Messages
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Error Reporting
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

ADMINS = [
    ("DC Errors", "errors@datacentral.org.au"),
]  # emails to send 5**s to
SERVER_EMAIL = "errors@datacentral.org.au"  # emails to send errors from
MANAGERS = [
    ("DC Missing", "missing@datacentral.org.au"),
]  # emails to send 404s to
IGNORABLE_404_URLS = [
    re.compile(r"\.(php|cgi)$"),
    re.compile(r"^/phpmyadmin/"),
    re.compile(r"wp-content"),
]  # regex of paths to not send emails about when 404


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           TEAM INFO
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DC_USER_TEAM_BLACKLIST_FILTER = {
    "dc",  # To cover dc-admin
    "asvo",  # To cover asvo-admin
}
