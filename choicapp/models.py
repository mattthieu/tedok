from django.db import models


class Item(models.Model):
    description = models.CharField(max_length=500)
    visibility = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True


class Ressource(Item):
    link = models.URLField(max_length=200, blank=True, null=True)


class Proposition(Item):
    type_of_vote = models.CharField(max_length=200, blank=True, null=True)
