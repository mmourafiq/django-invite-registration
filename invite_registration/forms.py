# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from invite_registration.fields import InvitationCodeField
from invite_registration.models import Invitation, InviteRequest
attrs_dict = {'class': 'required'}

class InvitationForm(forms.Form):
    email = forms.EmailField()

class RegistrationFormInvitation(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """    
    username = forms.RegexField(regex=r'^[\w.-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid':
                                                _("This value may contain only letters, numbers and ./-/_ characters.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                             label=_("E-mail"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                min_length = 8,
                                error_messages={'invalid': _(u"Minimum 8 caractères.")},
                                label=_("Password"))    
    code = forms.CharField(required=True, max_length=6,                              
                               label=_(u"Invitation code"))         
    honeypot = forms.CharField(required=False,
                                    label=_('If you enter anything in this field '\
                                            'your comment will be treated as spam'))  
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']
    
    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value    
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']    
    
    def clean(self):
        """
        Validate that the supplied email and the invitation code        
        """
        if 'code' in self.cleaned_data and 'email' in self.cleaned_data:            
            try:
                Invitation.objects.get(email=self.cleaned_data['email'], code=self.cleaned_data['code'])
            except Invitation.DoesNotExist:
                InviteRequest.objects.get_or_create(email=self.cleaned_data['email'])            
                raise forms.ValidationError(_("Ooops the invitation code is invalid."))
        return self.cleaned_data