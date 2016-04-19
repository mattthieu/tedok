from django.shortcuts import render, redirect, get_object_or_404
from choicapp.models import Value, Item_Voted, LogBookPost
from choicapp.forms import ValueForm, LogBookPostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from datetime import date
from django.contrib import messages 


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
        values.append((value, is_up_votable, is_down_votable, value.points))
    sorted_values = sorted(values, key=lambda tup: tup[3], reverse=True)
    context['values'] = sorted_values
    return render(request, 'choicapp/manifesti.html', context=context)


def show_ressources(request):
    context = {}
    return render(request, 'choicapp/ressources.html', context=context)


def show_logbook(request, *args, **kwargs):
    context = {}
    posts = []
    try:
        max_date = max([post.date for post in LogBookPost.objects.all()])
    except:
        max_date = date(2004, 3, 28)
    for post in LogBookPost.objects.all():
        if post.date == max_date:
            editable = True
        else:
            editable = False
        posts.append((post, editable))
    context = {'posts': posts}
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


class AddValue(View):
    '''class based view to add/edit Value.'''
    form_class = ValueForm
    model = Value
    template_name = 'choicapp/add_value.html'
    template_redirect = '/'
    template_details = 'choicapp/workshop_description.html'
    object_name = 'value_id'

    def get(self, request, *args, **kwargs):
        if self.object_name in kwargs.keys():
            instance = get_object_or_404(self.model,
                                         pk=kwargs[self.object_name])
            object_id = kwargs[self.object_name]
        else:
            instance = self.model()
            object_id = []
        if request.user.is_authenticated():
            form = self.form_class(instance=instance)
            return render(request, self.template_name,
                          {'form': form, self.object_name: object_id})
        else:
            return redirect(self.template_redirect)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if self.object_name in kwargs.keys():
            instance = get_object_or_404(self.model,
                                         pk=kwargs[self.object_name])
            object_id = kwargs[self.object_name]
        else:
            instance = self.model()
            object_id = []
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            # <process form cleaned data>
            try:
                w = form.save()
                w.save()
                return redirect(self.template_redirect)
            except:
                pass
        return render(request, self.template_name,
                      {'form': form, self.object_name: object_id})


class AddLogBookPost(View):
    '''class based view to add/edit a logbook post.'''
    form_class = LogBookPostForm
    model = LogBookPost
    template_name = 'choicapp/add_logbook_post.html'
    template_redirect = '/logbook'
    template_details = 'choicapp/workshop_description.html'
    object_name = 'logbookpost_id'

    def get(self, request, *args, **kwargs):
        if self.object_name in kwargs.keys():
            instance = get_object_or_404(self.model,
                                         pk=kwargs[self.object_name])
            object_id = kwargs[self.object_name]
        else:
            instance = self.model()
            object_id = []
        if request.user.is_authenticated():
            form = self.form_class(instance=instance)
            return render(request, self.template_name,
                          {'form': form, self.object_name: object_id})
        else:
            return redirect(self.template_redirect)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # precompute the most recent date among other blog posts
        try:
            max_date = max([post.date for post in LogBookPost.objects.all()])
        except:
            max_date = date(2004, 3, 28)

        if self.object_name in kwargs.keys():
            instance = get_object_or_404(self.model,
                                         pk=kwargs[self.object_name])
            object_id = kwargs[self.object_name]
            # make sure blog post is not too old
            # old posts are not editable
            if instance.date < max_date:
                return redirect(self.template_redirect)
        else:
            instance = self.model()
            object_id = []
            # Cannot add another blog post when another was opened the same day
            if date.today() == max_date:
                messages.error(request, 'You cannot post twice the same day.\
                                         Please edit the most recent post.')
                return redirect(self.template_redirect)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            # <process form cleaned data>
            try:
                w = form.save(commit=False)
                # check that we are not modifying an existing post
                # if we create from scratch, then set the date to toda
                if self.object_name in kwargs.keys():
                    w.date = date.today()
                w.save()
                return redirect(self.template_redirect)
            except:
                pass
        return render(request, self.template_name,
                      {'form': form, self.object_name: object_id})
