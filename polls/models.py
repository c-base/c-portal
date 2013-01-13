from django.db import models

from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date-published', auto_now_add=True)
    end_date = models.DateTimeField('open until', null=True)
    participants = models.ManyToManyField(User, null=True, default=None)

    def __unicode__(self):
        return self.question

    def currently_open(self):
        return tz.now() <= self.end_date


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice
