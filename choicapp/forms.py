from django.forms import ModelForm
from choicapp.models import Value, LogBookPost


class ValueForm(ModelForm):
    class Meta:
        model = Value
        exclude = ('points',)


class LogBookPostForm(ModelForm):
    class Meta:
        model = LogBookPost
        exclude = ('date',)
