from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Voter(models.Model):
    user = models.OneToOneField(User)
    dokv = models.IntegerField(default=100)
    dokp = models.IntegerField(default=0)

    def get_doks(self, dok_type):
        if dok_type == 'value':
            return self.dokv
        elif dok_type == 'proposition':
            return self.dokp
        else:
            raise(ValueError, 'Unknown type of doks')

    def set_doks(self, dok_type, amount):
        if dok_type == 'value':
            self.dokv = amount
        elif dok_type == 'proposition':
            self.dokp = amount
        else:
            raise(ValueError, 'Unknown type of doks')


class Item(models.Model):
    title = models.CharField(max_length=500)
    points = models.IntegerField(default=0)
    description = models.TextField(default='')

    def get_type(self):
        return 'item'


class Value(Item):
    def get_absolute_url(self):
        return reverse('choicapp:manifesti')

    def get_type(self):
        return 'value'


class Proposition(Item):
    deadline = models.DateField(help_text='DD/MM/YYYY')

    def get_absolute_url(self):
        return reverse('choicapp:propositions')

    def get_type(self):
        return 'proposition'


class Item_Voted(models.Model):
    item = models.ForeignKey(Item)
    voter = models.ForeignKey(Voter)
    points_given = models.IntegerField(default=0)
    vote_given = models.IntegerField(default=0)

    class Meta:
            unique_together = ('item', 'voter')


class LogBookPost(models.Model):
    date = models.DateField()
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('choicapp:logbook')


class Glossary_Word(models.Model):
    word = models.CharField(max_length=100)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('choicapp:glossary')
