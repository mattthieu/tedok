from django.shortcuts import render, redirect
from choicapp.models import Value, Voter, Item_Voted
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
                if request.user.voter.value_pts > 0:
                    is_up_votable = True
                if len(request.user.voter.item_voted_set.filter(item=value)):
                    is_down_votable = True
            except:
                pass
        values.append((value, is_up_votable, is_down_votable))
    context['values'] = values
    print(values)
    return render(request, 'choicapp/manifesti.html', context=context)


def show_ressources(request):
    context = {}
    return render(request, 'choicapp/ressources.html', context=context)


def show_logbook(request):
    context = {}
    return render(request, 'choicapp/logbook.html', context=context)


def show_propositions(request):
    context = {}
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
    value = Value.objects.get(pk=kwargs['value_id'])
    voter = request.user.voter
    # make sure the user still has some points
    if request.user.voter.value_pts > 0:
        try:
            i = Item_Voted.objects.get(voter=voter, item=value)
        except:
            i = Item_Voted(item=value, voter=voter)
        i.points_given += 1
        i.save()
        voter.value_pts += -1
        voter.save()
        value.points += 1
        value.save()
    return redirect('/manifesti')


@login_required
def down_value(request, *args, **kwargs):
    value = Value.objects.get(pk=kwargs['value_id'])
    voter = request.user.voter
    # make sure the user has already voted
    try:
        i = Item_Voted.objects.get(voter=voter, item=value)
        i.points_given += -1
        i.save()
        voter.value_pts += +1
        voter.save()
        value.points += -1
        value.save()
    except:
        pass
    # Delete Item voted is no points left
    if i.points_given <= 0:
        i.delete()
    return redirect('/manifesti')
