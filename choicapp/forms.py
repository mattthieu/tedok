from django.forms import ModelForm
from choicapp.models import Value


class ValueForm(ModelForm):
    class Meta:
        model = Value
        exclude = ('points',)
