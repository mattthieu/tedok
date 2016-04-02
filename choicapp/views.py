from django.shortcuts import render
from choicapp.models import Ressource


def index(request):
    context = {}
    context['ressources'] = Ressource.objects.all()
    return render(request, 'choicapp/index.html', context=context)
