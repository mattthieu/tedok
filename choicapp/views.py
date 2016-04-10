from django.shortcuts import render, redirect
from choicapp.models import Ressource, Proposition, Value, Voter, Item_Voted
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    context = {}
    return render(request, 'choicapp/index.html', context=context)


def show_manifesti(request):
    context = {}
    values = []
    for value in Value.objects.all():
        is_up_votable = False
        is_down_votable = False
        if request.user.is_authenticated():
            try:
                if request.user.voter.value_visibility_pts > 0:
                    is_up_votable = True
                if len(request.user.voter.item_voted_set.filter(item=value)):
                    is_down_votable = True
            except:
                pass
        values.append((value, is_up_votable, is_down_votable))
    context['values'] = values
    return render(request, 'choicapp/manifesti.html', context=context)


def show_ressources(request):
    context = {}
    ressources = []
    for ressource in Ressource.objects.all():
        is_up_votable = False
        is_down_votable = False
        if request.user.is_authenticated():
            try:
                if request.user.voter.ressource_visibility_pts > 0:
                    is_up_votable = True
                if ressource in request.user.voter.item.set_all():
                    is_down_votable = True
            except:
                pass
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


@login_required
def up_value(request, *args, **kwargs):
    value_id = kwargs['value_id']
    voter_id = kwargs['voter_id']
    value = Value.objects.get(pk=value_id)
    voter = Voter.objects.get(pk=voter_id)
    # check voter is the good one
    if request.user.voter == voter:
        # make sure the user still has some visibility points
        if voter.value_visibility_pts > 0:
            i = Item_Voted(item=value, voter=voter)
            i.save()
            voter.value_visibility_pts += -1
            voter.save()
        else:
            error = 'Tu n\'as pas assez de points. Enlève ton vote sur un autre item.'
    else:
        error = 'Mauvais utilisateur.'
    return redirect('/manifesti')
