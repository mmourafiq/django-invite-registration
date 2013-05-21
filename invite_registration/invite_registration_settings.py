# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''
from django.conf import settings

INITIAL_NUMBER_INVITATIONS = getattr(settings, 'INVITE_INITIAL_NUMBER_INVITATIONS', 0)
ENABLE_BETA = getattr(settings, 'INVITE_ENABLE_BETA', True)
NEVER_ALLOW_VIEWS = getattr(settings, 'INVITE_NEVER_ALLOW_VIEWS', [])
ALWAYS_ALLOW_VIEWS = getattr(settings, 'INVITE_ALWAYS_ALLOW_VIEWS', [])
ALWAYS_ALLOW_MODULES = getattr(settings, 'INVITE_ALWAYS_ALLOW_MODULES', [])
REDIRECT_URL = getattr(settings, 'INVITE_REDIRECT_URL', '/')
