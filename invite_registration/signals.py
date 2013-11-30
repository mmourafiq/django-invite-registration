# -*- coding: utf-8 -*-
from django.dispatch import Signal

invitation_sent = Signal()

invitation_accepted = Signal(providing_args=['inviting_user', 'invited_user'])
