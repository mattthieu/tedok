from django.db import models
from django.contrib.auth.models import User


class Voter(models.Model):
    user = models.OneToOneField(User)
    value_pts = models.IntegerField(default=100)


class Item(models.Model):
    description = models.CharField(max_length=500)
    points = models.IntegerField(default=0)


class Value(Item):
    definition = models.CharField(max_length=1000, blank=True, null=True)


class Item_Voted(models.Model):
    item = models.ForeignKey(Item)
    voter = models.ForeignKey(Voter)
    points_given = models.IntegerField(default=0)

    class Meta:
            unique_together = ('item', 'voter')


class LogBookPost(models.Model):
    date = models.DateField()
    content = models.TextField()
