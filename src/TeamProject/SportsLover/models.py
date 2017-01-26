from __future__ import unicode_literals

from datetime import timedelta
from django.db.models import Max
from django.utils import timezone
from django.utils.html import escape
from django.db import models
from django.contrib.auth.models import User


# a sport class: ball, water sports
class SportsClass(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


# represents a sport: basketball, baseball
class SportsItem(models.Model):
    item = models.CharField(max_length=40)
    label = models.ManyToManyField(SportsClass)

    def __str__(self):
        return self.item


class Place(models.Model):
    name = models.CharField(max_length=40, default="")
    address = models.CharField(max_length=100, default="")
    visitor = models.ManyToManyField(User)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0)
    rank = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0)

    def __str__(self):
        return self.name

class PlaceImage(models.Model):
    place = models.ForeignKey(Place)
    image = models.ImageField(upload_to='photos', null = True, blank = True)

class Group(models.Model):
    subject = models.CharField(max_length=50, default="")
    owner = models.ForeignKey(User, related_name='owner')
    member = models.ManyToManyField(User, related_name='member')
    place = models.ForeignKey(Place)
    address = models.CharField(max_length=100, default="")
    sportsitem = models.ForeignKey(SportsItem)
    sportsclass = models.ForeignKey(SportsClass)
    size = models.IntegerField(default=1)
    introduction = models.CharField(max_length=400, default="")
    cost = models.DecimalField(max_digits=5, default=0.0, decimal_places=2)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner


class Info(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user = models.OneToOneField(User)
    age = models.CharField(max_length=20, default="", blank=True)
    bio = models.CharField(max_length=420, default="", blank=True)
    image = models.ImageField(upload_to='photos', default='empty.png', blank=True)

    def __unicode__(self):
        return self.user


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='has_chats')
    content = models.TextField()
    deleted = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)
    group = models.CharField(max_length=50, default="")

    def __unicode__(self):
        return u'%s' % self.content

    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00", group_id=0):
        return Chat.objects.filter(time__gt=time, group__exact=group_id).distinct()

    @staticmethod
    def get_chats(time="1970-01-01T00:00+00:00", group_id=0):
        return Chat.objects.filter(deleted=False,
                                   time__gt=time, group__exact=group_id).distinct()

    @property
    def html(self):
        return "<p id='chat_%d'><b>%s %s says:</b> %s </p>" % (self.id, escape((self.time - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
                                                               escape(self.sender.username), escape(self.content))

    @staticmethod
    def get_max_time():
        return Chat.objects.all().aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"


class GroupNotification(models.Model):
    reciever = models.ForeignKey(User, related_name='group_reciever')
    sender = models.ForeignKey(User, related_name='group_sender')
    content = models.CharField(max_length=100, default="")
    group = models.OneToOneField(Group)
    types = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return self.reciever


class Friend(models.Model):
    user = models.OneToOneField(User, related_name='user')
    friend = models.ManyToManyField(User, related_name='friend')

    def __unicode__(self):
        return self.user


class FriendNotification(models.Model):
    reciever = models.ForeignKey(User, related_name='reciever_friend')
    sender = models.ForeignKey(User, related_name='sender_friend')
    content = models.CharField(max_length=100, default="")
    types = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return self.reciever

class Notification(models.Model):
    reciever = models.ForeignKey(User, related_name='reciever')
    content = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100, default="incomplete")
    types = models.CharField(max_length=20, default="")
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.reciever

class Cost(models.Model):
    place = models.ForeignKey(Place, related_name='cost_place')
    cost = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0)
    def __str__(self):
        return self.cost

class Rank(models.Model):
    place = models.ForeignKey(Place, related_name='place')
    rank = models.IntegerField(default=5)
    def __str__(self):
        return self.rank

class Comment(models.Model):
    place = models.ForeignKey(Place, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text








