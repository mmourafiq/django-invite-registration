# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: 
'''
import datetime
import random
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.db import models
from invite_registration import signals
from invite_registration.settings import INITIAL_NUMBER_INVITATIONS

DEFAULT_ALPHABET = 'az7er5tyu1io0pq4sd9fg6hjk8lmw3xcv2bn'

class InviteRequest(models.Model):
    email = models.EmailField(_('Email address'), unique=True)

class Invitation(models.Model):
    """
    Invitation model
    """
    code = models.CharField(blank=True, max_length=6,
                            verbose_name=_(u"Invitation code"))    
    user = models.ForeignKey(User, verbose_name=_(u'Invitor'), 
                             related_name='invitations')
    email = models.EmailField(verbose_name=_(u"Email"))
    date_invited = models.DateTimeField(default=datetime.datetime.now,
                                        verbose_name=_(u'date invited'))
    
    class Meta:
        verbose_name = _(u'Invitation')
        verbose_name_plural = _(u'Invitations')
        ordering = ('-date_invited',)
    
    def __unicode__(self):
        return _('%(username)s invited %(email)s on %(date)s') % {
            'username': self.user.username,
            'email': self.email,
            'date': str(self.date_invited.date()),
        }
    
    def save(self,*args, **kwargs):
        if not self.id:
            self.code = ''.join(random.sample(DEFAULT_ALPHABET, 6)) 
        super(Invitation, self).save(*args, **kwargs)
    
    def accepted(self, invited_user):
        """
        increment number of accepted invitations
        invitation.signals.invitation_accepted``
        """
        self.user.invitation_use.accepted()
        signals.invitation_accepted.send(sender=self,
                                         inviting_user=self.user,
                                         invited_user=invited_user)
    accepted.alters_data = True
        
    def send_email(self, request=None):
        """
        Send invitation email.        
        ``invitation.signals.invitation_sent`` is sent on completion.
        """                
        if Site._meta.installed:
            site = Site.objects.get_current()
        elif request is not None:
            site = RequestSite(request)
        invitation_context = {'invitation': self, 'site': site}
        subject = render_to_string('iinvite_registration/invitation_email_subject.txt',
                                   invitation_context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('iinvite_registration/invitation_email.txt', 
                                   invitation_context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
        signals.invitation_sent.send(sender=self)    
        
class InvitationUse(models.Model):
    """
    Invitation use of user.
    """
    user = models.OneToOneField(User,
                                related_name='invitation_use')
    available = models.IntegerField(_(u'available invitations'),
                                    default=INITIAL_NUMBER_INVITATIONS)
    sent = models.IntegerField(_(u'invitations sent'), default=0)
    accepted = models.IntegerField(_(u'invitations accepted'), default=0)
    
    def __unicode__(self):
        return _(u'invitation use for %(username)s') % {
                                               'username': self.user.username}
    
    def can_send(self):
        return True if self.available > 0 else False    
    
    def sent(self):
        """
        user sent an invitation
        """
        self.available -= 1
        self.sent += 1
        self.save()
    sent.alters_data = True 
    
    def accepted(self):
        """
        a new invitation has been accepted                
        """       
        self.accepted += 1        
        self.save()
        
    accepted.alters_data = True
