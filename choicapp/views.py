from django.shortcuts import render, redirect
from choicapp.models import Ressource, Proposition
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    context = {}
    return render(request, 'choicapp/index.html', context=context)


def show_manifesti(request):
    context = {}
    return render(request, 'choicapp/manifesti.html', context=context)


def show_ressources(request):
    context = {}
    ressources = []
    for ressource in Ressource.objects.all():
        is_up_votable = False
        is_down_votable = False
        if request.user.is_authenticated():
            if request.user.voter.ressource_visibility_pts > 0:
                is_up_votable = True
            if ressource in request.user.voter.ressources_voted.set_all():
                is_down_votable = True
        ressources.append((ressource, is_up_votable, is_down_votable))
    context['ressources'] = ressources
    return render(request, 'choicapp/ressources.html', context=context)


def show_logbook(request):
    context = {}
    return render(request, 'choicapp/logbook.html', context=context)


def show_propositions(request):
    context = {}
    context['propositions'] = Proposition.objects.all()
    return render(request, 'choicapp/propositions.html', context=context)


def login_user(request):
    error = False
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,
                                password=password)
            if user:
                login(request, user)
            else:  # user is none
                error = True
    else:
        form = AuthenticationForm()
    return render(request, 'choicapp/login.html',
                  {'form': form, 'error': error})


def logout_user(request):
    logout(request)
    return redirect('/')
