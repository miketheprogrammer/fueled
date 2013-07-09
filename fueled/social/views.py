# Create your views here.
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
from accounts.models import TeamUser
from social.models import RestaurantVisits, RestaurantThumbsDown
from restaurants.models import Restaurant
from django.utils import simplejson

@login_required
def team(request):
    team_user = TeamUser.objects.get(user=request.user)
    team = team_user.team
    team_mates = TeamUser.objects.filter(team=team)

    context = {
        'team_user': team_user,
        'team_mates': team_mates,
        'team_mates_count': team_mates.count(),
        'team': team
    }
    return render_to_response("team.html", RequestContext(request,context))

@login_required
def thumbs_toggle(request, restaurant_id):
    toggle = request.GET.get('v')
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    try:
        old_thumbs = RestaurantThumbsDown.objects.get(user=request.user, restaurant=restaurant)
        response = True
    except RestaurantThumbsDown.DoesNotExist as e:
        response = True
        old_thumbs = None
        print e
    if toggle == 'false':
        if old_thumbs is not None:
            old_thumbs.delete()
    if toggle == 'true':
        if old_thumbs is not None:
            response = False
        else:
            RestaurantThumbsDown.objects.create(user=request.user, restaurant=restaurant)
            response = True

    return HttpResponse(simplejson.dumps({"success":response}))


    
