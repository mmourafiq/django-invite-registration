# -*- coding: utf-8 -*-
'''
Created on Oct 01, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers:
'''
from django.conf.urls import patterns, include, url
from invite_registration import views  

urlpatterns = patterns('',                                
    url(r'^invite/$', views.invite, name='invitation_invite'),        
    )