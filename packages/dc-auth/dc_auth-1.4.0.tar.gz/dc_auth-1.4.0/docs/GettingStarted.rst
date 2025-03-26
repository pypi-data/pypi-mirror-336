.. _getting-started:

Getting started
###############

Quick start
-----------

.. note::
    This assumes you are using the CAS protocol to provide authentication.

Add "dc_auth" + the following apps to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dc_auth',
    ]

Add django_settings_export.settings_export to your project's
context_processors::

    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django_settings_export.settings_export',                   # <----
        ],
    },

Include the dc_auth URLconf in your project urls.py like this::

    path('auth/', include('dc_auth.urls')),

Migrate to create the Profile table. Run `python manage.py migrate`.

Start the development server and visit `auth/login` to log into your account.

Tests
-----

From the top-level directory run:

.. code-block::

    $ tox

dcauth comes with some helpers that tools building on dcauth can use,
specifically pytest fixtures for affiliation (`affiliation`) and test passwords
(`secure_password`), as well as factories and fixtures for the `User` and
`Profile` classes.

Installing for internal applications
------------------------------------

To install into another Data Central project, add `dc_auth` to your requirements
file (lock to a specific version), and ensure that pip is pointed to the DC
devpi instance.


Contributing
------------

For local development (within a virtualenv), run the following to get a django
test web server (`dc_auth.settings_testing` is for running the tests, but should
be fine for interactive use).

.. code-block::

    $ export DJANGO_SETTINGS_MODULE=dc_auth.settings_testing
    $ pip install -e .
    $ python -m django runserver
