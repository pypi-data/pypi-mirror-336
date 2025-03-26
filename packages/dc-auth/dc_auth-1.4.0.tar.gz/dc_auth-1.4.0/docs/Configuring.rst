.. _configuring:

Configuring
###########

If you choose to use the CAS protocol (which should be used if possible),
then importing the settings file `dc_auth.settings` will provide all the
settings required to use CAS in production (development CAS is only needed if
you are developing apps talking directly to LDAP).

For OAuth 2/OIDC, there are some additional settings that must be provided.


OAuth 2/OIDC basic configuration
--------------------------------
In order to validate access tokens created by CAS, you will need a client ID and
client secret. Ask on Slack about this.

These should be added to the settings file as::

    DC_OAUTH2_RESOURCE_CLIENT_ID = client_id
    DC_OAUTH2_RESOURCE_CLIENT_SECRET = client_secret

Additionally, to use the OAuth2/OIDC authentication backend, you will need to
change the backends used in the settings file to::

    AUTHENTICATION_BACKENDS = [
        'dc_auth.backends.OAuth2ResourceBackend'
    ]

While it should be possible to use both backends at once, this hasn't been
tested yet.
