"""myEWB mailchimp integration

This file is part of myEWB
Copyright 2010 Engineers Without Borders Canada

@author: Francis Kung <franciskung@ewb.ca>
"""

from django.contrib.auth.models import User
from django.db import models

from base_groups.models import BaseGroup

# add the mailchimp dynamically here, so we don't clutter the BaseGroup code...
BaseGroup.add_to_class('mailchimp', models.BooleanField(default=False))

# base model.  Only to reduce typing..,.
class MailchimpEvent(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True
        
# List events: subscribes and unsubscribes to the main list.
class ListEventManager(models.Manager):
    def subscribe(self, user):
        # if they have a pending unsubscribe, this event will cancel it out
        unsub = self.filter(user=user,
                            subscribe=False)
        if unsub.count():
            for u in unsub:
                u.delete()
            return True
        
        return self.create(user=user,
                           subscribe=True)
    
    def unsubscribe(self, user):
        # if they have a pending subscribe, this event will cancel it out
        unsub = self.filter(user=user,
                            subscribe=True)
        if unsub.count():
            for u in unsub:
                u.delete()
            return True
        
        return self.create(user=user,
                           subscribe=False)
        
class ListEvent(MailchimpEvent):
    # true if this is a subscribe event; false if it is an unsubscribe
    subscribe = models.BooleanField()
    objects = ListEventManager()

# Group events: joining or leaving specific groups.
class GroupEventManager(models.Manager):
    def join(self, user, groupname):
        # if they have a pending unsubscribe, then this is pointless
        unsub = ListEvent.objects.filter(user=user,
                                         subscribe=False)
        if unsub.count():
            return False
        
        # if they have a pending leave, this event will cancel it out
        unsub = self.filter(user=user,
                            groupname=groupname,
                            join=False)
        if unsub.count():
            for u in unsub:
                u.delete()
            return True
        
        return self.create(user=user,
                           groupname=groupname,
                           join=True)
    
    def leave(self, user, groupname):
        # if they have a pending unsubscribe, then this is pointless
        unsub = ListEvent.objects.filter(user=user,
                                         subscribe=False)
        if unsub.count():
            return False
        
        # if they have a pending join, this event will cancel it out
        unsub = self.filter(user=user,
                            groupname=groupname,
                            join=True)
        if unsub.count():
            for u in unsub:
                u.delete()
            return True
        
        return self.create(user=user,
                           groupname=groupname,
                           join=False)
        
    
class GroupEvent(MailchimpEvent):
    # true if this is a join event; false if it is a leave event
    join = models.BooleanField()
    groupname = models.CharField(max_length=255, blank=True, null=True)
    objects = GroupEventManager()

# Profile events: updating your profile info.
class ProfileEventManager(models.Manager):
    def update(self, user):
        # if they are in the (un)subscribe queue, they don't need to be updated...
        sub = ListEvent.objects.filter(user=user)
        if sub.count():
            return True
        
        return self.create(user=user)
        
class ProfileEvent(MailchimpEvent):
    objects = ProfileEventManager()
