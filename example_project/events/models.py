import datetime
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField(default=datetime.datetime.today().date())

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u'/events/%s/' % self.id
