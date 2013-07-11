from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import get_current_site
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, NoReverseMatch, resolve
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from accounts.forms import UserForm, UserCreationForm, UserEditForm
from accounts.models import TeamUser
from social.models import Team

def login(request):
    context = {}
    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect(reverse("dashboard.views.index"))
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('fueled.views.home'))
    if 'user_form' not in context:
        context['user_form'] = UserForm()
    return render_to_response('login.html', RequestContext(request, context))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("accounts.views.login"));

def new(request):
    context = {}
    if request.method == "POST":
        userform = UserCreationForm(data=request.POST)
        if userform.is_valid():
            user = User.objects.create_user(userform.cleaned_data['username'], 
                                     userform.cleaned_data['email'],
                                     userform.cleaned_data['password'])
            try:
                team = Team.objects.get(name=request.POST['team'])
            except:
                team = Team(name=request.POST['team'])
                team.save()
            team_user = TeamUser(team=team, user=user)
            team_user.save()
                
            if request.POST.get("isadmin", False):
                user.groups.add(Group.objects.get(name="Administrator"))
            else:
                user.groups.add(Group.objects.get(name="Standard User"))

            return HttpResponseRedirect(reverse('accounts.views.login'))
        else:
            print userform.errors
        pass

    context['new_user_form'] = UserCreationForm()
    return render_to_response("new.html", RequestContext(request, context))


@login_required
def edit(request):
    context = {}
    edit_form = UserEditForm(instance=request.user)
    if request.method == "POST":
        userform = UserEditForm(data=request.POST, instance=request.user)
        if userform.is_valid():
            
            try:
                team = Team.objects.get(name=request.POST['team'])
            except:
                team = Team.objects.create(name=request.POST['team'])
            try:
                old_team = TeamUser.objects.get(user=request.user)
            except:
                old_team = TeamUser.objects.none()


            if not old_team or old_team.team.name != team.name:
                old_team.delete()
                print old_team
                team_user = TeamUser.objects.create(team=team, user=request.user)
            
            
            user = userform.save()
            user.set_password(user.password)
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save();
            
            return HttpResponseRedirect(reverse('dashboard.views.index'))
        else:
            edit_form = userform
            print userform.errors
        pass
    return render_to_response('edit.html', RequestContext(request, {'form': edit_form}))
