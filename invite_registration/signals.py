# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''
from django.dispatch import Signal

invitation_sent = Signal()

invitation_accepted = Signal(providing_args=['inviting_user', 'invited_user'])