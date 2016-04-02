from django.shortcuts import render
from choicapp.models import Ressource, Proposition


def index(request):
    context = {}
    return render(request, 'choicapp/index.html', context=context)


def show_manifesti(request):
    context = {}
    return render(request, 'choicapp/manifesti.html', context=context)


def show_ressources(request):
    context = {}
    context['ressources'] = Ressource.objects.all()
    return render(request, 'choicapp/ressources.html', context=context)


def show_logbook(request):
    context = {}
    return render(request, 'choicapp/logbook.html', context=context)


def show_propositions(request):
    context = {}
    context['propositions'] = Proposition.objects.all()
    return render(request, 'choicapp/propositions.html', context=context)
