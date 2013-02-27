# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from invite_registration.models import InvitationUse, Invitation, InviteRequest


class InvitationUseAdmin(admin.ModelAdmin):
    fields = ('user', 'available', 'sent', 'accepted')    
    list_display = ('user', 'available', )
    list_filter = ('user', 'available', )    

admin.site.register(InvitationUse, InvitationUseAdmin)

class InvitationAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    fields = ('code', 'user', 'email', 'date_invited', )    
    list_display = ('code', 'user', 'email', 'date_invited', )
    list_filter = ('code', 'user', 'email', 'date_invited', )
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(InviteRequest)