# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from registration import signals
from registration.models import RegistrationProfile
from invite_registration.forms import RegistrationFormInvitation as RegistrationForm
from invite_registration.models import Invitation, InvitationUse

class InviteOnlyBackend(object):
    """
    A registration backend which follows an invitation workflow:

    1. User request an invitation
    
    2. User signs up, account is created and activated since the 
       user already introduces invitation code.    
    
    3. USer is authenticated    

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``INVITATION_CODE_DAYS`` be supplied, specifying
      (as an integer) the number of days from receiving the invitation
       during which a user may activate their account (after that period
      expires, activation will be disallowed).

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.    
    
    """
    def register(self, request, **kwargs):
        """
        A registration backend which implements the simplest possible
        workflow: a user supplies a username, email address, password and
        invitation code. A user is immediately signed
        up and logged in.
        """
        username, email, password, code = kwargs['username'], \
            kwargs['email'], kwargs['password'], kwargs['code']                    
        User.objects.create_user(username, email, password)        
        invitation = Invitation.objects.get(code=code, email=email)                                
        new_user = authenticate(username=username, password=password)
        InvitationUse.objects.create(user=new_user)        
        invitation.accepted(new_user)        
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user            

    def activate(self, **kwargs):
        raise NotImplementedError

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.        
        """
        return RegistrationForm

    def post_registration_redirect(self, request, user):
        """        
        After registration, redirect to the user's account page.        
        """
        return (user.get_absolute_url(), (), {})

    def post_activation_redirect(self, request, user):
        raise NotImplementedError
