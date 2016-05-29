from django.shortcuts import render, redirect, get_object_or_404
from choicapp.models import Value, Item_Voted, LogBookPost, Glossary_Word, Item
from choicapp.models import Proposition
from choicapp.forms import ValueForm, LogBookPostForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from datetime import date
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from tedok.settings import BIG_POINTS


def index(request):
    context = {}
    return render(request, 'choicapp/index.html', context=context)


def items_pointable(user, dok_type, item_list):
    '''
    Return a the items with variables saying whether they can be
    up/down voted for visibility (which is called up/down pointable).
    '''
    extended_item_list = []
    for item in item_list:
        is_up_pointable = False
        is_down_pointable = False
        is_big_up_pointable = False
        is_big_down_pointable = False
        nb_pts_given = 0
        if user.is_authenticated():
            if user.voter.get_doks(dok_type) > 0:
                    is_up_pointable = True
            if user.voter.get_doks(dok_type) > BIG_POINTS - 1:
                    is_big_up_pointable = True
            try:
                nb_pts_given = user.voter.item_voted_set\
                    .get(item=item).points_given
                if nb_pts_given > 0:
                    is_down_pointable = True
                if nb_pts_given > BIG_POINTS - 1:
                    is_big_down_pointable = True
            except:
                pass
        extended_item_list.append((item, is_up_pointable, is_down_pointable,
                                   is_big_up_pointable, is_big_down_pointable,
                                   item.points, nb_pts_given))
    sorted_extended_item_list = sorted(extended_item_list,
                                       key=lambda tup: tup[-2], reverse=True)
    return sorted_extended_item_list


def show_manifesti(request):
    context = {}
    context['values'] = items_pointable(user=request.user,
                                        dok_type='value',
                                        item_list=Value.objects.all())
    context['big_pts'] = BIG_POINTS
    return render(request, 'choicapp/manifesti.html', context=context)


def show_ressources(request):
    context = {}
    return render(request, 'choicapp/ressources.html', context=context)


class GlossaryWordCreate(CreateView):
    model = Glossary_Word
    fields = '__all__'
    template_name_suffix = '_form'


class GlossaryWordUpdate(UpdateView):
    model = Glossary_Word
    fields = '__all__'
    template_name_suffix = '_form'


def show_glossary(request):
    context = {}
    words = Glossary_Word.objects.all()
    context['words'] = words
    return render(request, 'choicapp/glossary.html', context=context)


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
    propositions = items_pointable(user=request.user,
                                   dok_type='proposition',
                                   item_list=Proposition.objects.all())
    print(propositions)
    new_propositions = []
    for extended_proposition in propositions:
        proposition = extended_proposition[0]
        nb_up_votes = len(proposition.item_voted_set
                          .filter(vote_given=1))
        nb_down_votes = len(proposition.item_voted_set
                            .filter(vote_given=-1))

        # default values
        up_voted = False
        down_voted = False
        # if user is authenticated then set personnalized details
        if request.user.is_authenticated():
            try:
                i = proposition.item_voted_set.get(voter=request.user.voter)
                if i.vote_given == 1:
                    up_voted = True
                    down_voted = False
                elif i.vote_given == -1:
                    up_voted = False
                    down_voted = True
                else:
                    up_voted = False
                    down_voted = False
            except:
                up_voted = False
                down_voted = False
        new_propositions.append(extended_proposition +
                                (up_voted, down_voted,
                                 nb_up_votes, nb_down_votes))
    context = {}
    context['propositions'] = new_propositions
    context['big_pts'] = BIG_POINTS
    return render(request, 'choicapp/propositions.html', context=context)


@login_required
def up_visibility(request, *args, **kwargs):
    item = Item.objects.get(pk=kwargs['item_id'])
    # finds whether value or proposition
    # TODO: find more elegant method!!!!
    try:
        item_type = item.value.get_type()
        redirection = '/manifesti'  + '#' + str(kwargs['item_id'])
    except:
        pass
    try:
        item_type = item.proposition.get_type()
        redirection = '/propositions' + '#' + str(kwargs['item_id'])
    except:
        pass
    nb_votes = int(kwargs['nb_votes'])
    voter = request.user.voter
    # make sure the user still has some points
    voter_pts = request.user.voter.get_doks(item_type)
    if voter_pts >= nb_votes:
        try:
            i = Item_Voted.objects.get(voter=voter, item=item)
        except:
            i = Item_Voted(item=item, voter=voter)
        i.points_given += nb_votes
        i.save()
        voter.set_doks(item_type, voter_pts - nb_votes)
        voter.save()
        item.points += nb_votes
        item.save()
    return redirect(redirection)


@login_required
def down_visibility(request, *args, **kwargs):
    item = Item.objects.get(pk=kwargs['item_id'])
    # finds whether value or proposition
    # TODO: find more elegant method!!!!
    try:
        item_type = item.value.get_type()
        redirection = '/manifesti' + '#' + str(kwargs['item_id'])
    except:
        pass
    try:
        item_type = item.proposition.get_type()
        redirection = '/propositions' + '#' + str(kwargs['item_id'])
    except:
        pass
    nb_votes = int(kwargs['nb_votes'])
    voter = request.user.voter
    voter_pts = request.user.voter.get_doks(item_type)
    # make sure the user has already voted
    try:
        i = Item_Voted.objects.get(voter=voter, item=item)
        if i.points_given >= nb_votes:
            i.points_given += -nb_votes
            i.save()
            voter.set_doks(item_type, voter_pts + nb_votes)
            voter.save()
            item.points += -nb_votes
            item.save()
        # Delete Item voted is no points left
        if i.points_given <= 0:
            i.delete()
    except:
        pass
    return redirect(redirection)


@login_required
def updown_proposition(request, *args, **kwargs):
    prop = Proposition.objects.get(pk=kwargs['proposition_id'])
    print(kwargs)
    if kwargs['vote'] == '1':
        vote = 1
    elif kwargs['vote'] == '0':
        vote = -1
    else:
        redirect('/propositions')
    voter = request.user.voter
    try:
        i = Item_Voted.objects.get(voter=voter, item=prop)
    except:
        i = Item_Voted(item=prop, voter=voter)
    i.vote_given = vote
    i.save()
    print(i.vote_given)
    return redirect('/propositions')


class AddLogBookPost(View):
    '''class based view to add/edit a logbook post.'''
    form_class = LogBookPostForm
    model = LogBookPost
    template_name = 'choicapp/add_logbook_post.html'
    template_redirect = '/logbook'
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
                if self.object_name not in kwargs.keys():
                    w.date = date.today()
                w.save()
                return redirect(self.template_redirect)
            except:
                pass
        return render(request, self.template_name,
                      {'form': form, self.object_name: object_id})


class PropositionCreate(CreateView):
    model = Proposition
    fields = ['title', 'description', 'deadline']
    template_name_suffix = '_form'

    def get_form(self, form_class):
        form = super(PropositionCreate, self).get_form(form_class)
        form.fields['deadline'].input_format = 'settings.DATE_INPUT_FORMATS'
        return form


class PropositionUpdate(UpdateView):
    model = Proposition
    fields = ['title', 'description', 'deadline']
    template_name_suffix = '_form'


class ValueCreate(CreateView):
    model = Value
    fields = ['title', 'description']
    template_name_suffix = '_form'


class ValueUpdate(UpdateView):
    model = Value
    fields = ['title', 'description']
    template_name_suffix = '_form'
