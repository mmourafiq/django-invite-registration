# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import simplejson
from models import Invitation, InviteRequest
from invite_registration.forms import InvitationForm
from invite_registration.settings import REDIRECT_URL


def request_invite(request, form_class=InvitationForm):
    """
    Allow a user to request an invite at a later date by entering their email address.
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            InviteRequest.objects.get_or_create(email=form.cleaned_data['email'])            
            if not request.is_ajax():  
                return HttpResponseRedirect(REDIRECT_URL)
            response = ({'success':True})
            json = simplejson.dumps(response, ensure_ascii=False)
            return HttpResponse(json, mimetype="application/json") 
        else:
            if not request.is_ajax():  
                return HttpResponseRedirect(REDIRECT_URL)
            response = ({'success':False})
            json = simplejson.dumps(response, ensure_ascii=False)
            return HttpResponse(json, mimetype="application/json")

@login_required
def invite(request, success_url=None, form_class=InvitationForm,
               template_name='invite_registration/invitation_form.html',
               extra_context=None):
    """
    Create an invitation and send invitation email.
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            #create a new invitation object
            #if already exists, then it just resend an email to the appropriate email
            invitation = Invitation.objects.get_or_create(
                                     request.user, form.cleaned_data["email"])            
            invitation.send_email(request=request)
            return HttpResponseRedirect(success_url or reverse('invitation_invite'))
    else:
        form = form_class()
    context = {'form': form}
    if extra_context is not None:
        context.update(extra_context)    
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))