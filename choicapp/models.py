from django.db import models
from django.contrib.auth.models import User


class Voter(models.Model):
    user = models.OneToOneField(User)
    ressource_visibility_pts = models.IntegerField(default=100)
    value_visibility_pts = models.IntegerField(default=100)


class Item(models.Model):
    description = models.CharField(max_length=500)
    visibility = models.IntegerField(default=0)


class Ressource(Item):
    link = models.URLField(max_length=200, blank=True, null=True)


class Proposition(Item):
    type_of_vote = models.CharField(max_length=200, blank=True, null=True)


class Value(Item):
    definition = models.CharField(max_length=1000, blank=True, null=True)


class Item_Voted(models.Model):
    item = models.ForeignKey(Item)
    voter = models.ForeignKey(Voter)
