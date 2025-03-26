.. dc_auth documentation master file, created by
   sphinx-quickstart on Tue Oct  1 16:22:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dc-auth documentation
=====================

`dcauth` provides both the authentication, groups and additional user properties
for Data Central django apps, but also base templates and other core django
support that Data Central django apps can use.

Apps can either use the CAS protocol or OAuth 2/OIDC to authenticate. Sessions
(if used) should be managed by django.


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    GettingStarted
    Configuring
    Reference

