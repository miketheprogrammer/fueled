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
from social.models import RestaurantVisits
from social.lib.recommend import BaseRecommendationEngine
@login_required
def index(request):
    team_user = TeamUser.objects.get(user=request.user)
    team = team_user.team
    team_mates = TeamUser.objects.filter(team=team).exclude(user=request.user)
    try:
        most_visited = RestaurantVisits.objects.filter(user=request.user).order_by('-visit_count')[:1][0]
    except IndexError:
        most_visited = None
        print 'This user has not visited any locations yet'
    team_most_visited = []
    for member in team_mates:
        try:
            member_most_visited = RestaurantVisits.objects.filter(
                user=member.user).order_by('-visit_count')[:1][0]
            
            team_most_visited.append(member_most_visited)
        except IndexError:
            print 'This teammate has not visited any restaurant yet'

    bre = BaseRecommendationEngine(request, team, 4)
    recommendation = bre.recommend(1)
    context = {
        'team_user': team_user,
        'team_mates': team_mates,
        'team_mates_count': team_mates.count()+1,#offset for exclude of user
        'team': team,
        'most_visited': most_visited,
        'team_most_visited': team_most_visited,
        'recommendation': recommendation,
        
    }
    return render_to_response("index.html", RequestContext(request,context))
