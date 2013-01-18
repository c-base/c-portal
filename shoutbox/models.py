from django.db import models

from c_portal.models import Project


class Box(models.Model):
    project = models.OneToOneField(Project)

    def __unicode__(self):
        return self.project.name

class Shout(models.Model):
    box = models.ForeignKey(Box)
    nickname = models.CharField(max_length=64)
    shout = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '#%s | %s: %s' % (self.box, self.nickname, self.shout)

