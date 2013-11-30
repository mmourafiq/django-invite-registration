# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from invite_registration import views  

urlpatterns = patterns('',                                
    url(r'^invite/$', views.invite, name='invitation_invite'), 
    url(r'^request/$', views.request_invite, name='invitation_request'),        
    )
