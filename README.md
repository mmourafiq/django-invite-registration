invite-registration
===================

This is a fairly simple invite-only backend for user-registration, designed to make private beta and user signups through invitation as painless as possible.

Overview
========

This reusable Django applications provides many useful things to a site under private (closed) beta:

* A form that allows users to enter their email address so that you can send
  them an invite or a site launch notification later.
* A middleware that locks the site down for non-logged in users.  If you
  control account creation this is a very effective way of limiting a site
  to beta testers only.
* A user invitation workflow:

    1. User fills out an invitation form, entering an email address.    
    2. An invitation code is created and sent to the email address.
    3. User is able to register in with the invitation code and begin contributing to your site.
    4. The new user has a quota restrictions.
    
Various methods of extending and customizing the invitation process are also provided.

Installation
============

In order to use invite-registration, you will need to have a functioning installation of Django 1.0 or newer; 
you will need user-registration (http://pypi.python.org/pypi/django-registration/)

To use the invite form, you first need to add ``invite-registration`` to
``INSTALLED_APPS`` in your settings file::

    INSTALLED_APPS = (
    ...
    'invite-registration',
    )

You will also need to add ::

    urlpatterns = patterns('',
        ...
        (r'^invite/', include('invite-registration.urls')),
        (r'^accounts/', include('invite-registration.backends.invite-only.urls')),
    )

Add the setting ``INVITE_INITIAL_NUMBER_INVITATIONS`` to your settings file; 
this should be the initial quota each new user has.

Create the necessary templates for user-registration
Create the necessary templates for invite-registration : 
  - invite_registration/invitation_form.html
  - invite_registration/invitation_email_subject.txt is used for the subject of the invitation email.
  - invite_registration/invitation_email.txt is used for the body of the invitation email.

Examples of all of these templates are not provided; you will need to create them yourself.

Closed beta middleware
======================

If you would also like to prevent non-logged-in users from viewing your site,
you can make use of ``invite-registration.middleware.PrivateBetaMiddleware``.  This
middleware redirects all views to a specified location if a user is not logged in.

To use the middleware, add it to ``MIDDLEWARE_CLASSSES`` in your settings file::

    MIDDLEWARE_CLASSES = (
        ...
        'privatebeta.middleware.PrivateBetaMiddleware',
    )

There are a few settings that influence behavior of the middleware:

``NEVER_ALLOW_VIEWS``
    A list of full view names that should *never* be displayed.  This
    list is checked before the others so that this middleware exhibits
    deny then allow behavior.

``ALWAYS_ALLOW_VIEWS``
    A list of full view names that should always pass through.

``ALWAYS_ALLOW_MODULES``
    A list of modules that should always pass through.  All
    views in ``django.contrib.auth.views``, ``django.views.static``
    and ``privatebeta.views`` will pass through unless they are
    explicitly prohibited in ``PRIVATEBETA_NEVER_ALLOW_VIEWS``

``REDIRECT_URL``
    The URL to redirect to.  Can be relative or absolute.
