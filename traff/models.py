from django.db import models

from django.utils import timezone

# Create your models here.

class Day(models.Model):
    dayID = models.IntegerField(default=0)
    date = models.DateField('Whole Day')
    dayTraffic = models.IntegerField()
    def __unicode__(self):
        return str(self.date)


class DayTime(models.Model):
    day = models.ForeignKey(Day)
    time = models.TimeField('Day time')
    traff = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % (self.time)