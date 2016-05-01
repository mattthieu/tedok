from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Voter(models.Model):
    user = models.OneToOneField(User)
    value_pts = models.IntegerField(default=100)


class Item(models.Model):
    title = models.CharField(max_length=500)
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


class Glossary_Word(models.Model):
    word = models.CharField(max_length=100)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('choicapp:glossary')


class Proposition(Item):
    description = models.TextField()
    deadline = models.DateField(help_text='DD/MM/YYYY')

    def get_absolute_url(self):
        return reverse('choicapp:propositions')
