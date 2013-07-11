# Create your views here.

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import get_current_site
from django.core.context_processors import csrf, csrf
from django.core.urlresolvers import reverse, NoReverseMatch, resolve
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils import simplejson
from restaurants.forms import RestaurantForm
from restaurants.models import Restaurant
from social.models import RestaurantVisits, RestaurantThumbsDown, RestaurantReview, RestaurantComment
import urllib


#this is a test for whether the user is an admin
#this could be in a better place, but nice to have here for demo purposes.
def UserIsAdmin(user):
    return bool(user.groups.filter(name="Administrator"))


@login_required
@user_passes_test(UserIsAdmin, login_url="/restaurants/all")
def create(request):
    context = {}

    if request.method == "POST":
        restaurant_form = RestaurantForm(data=request.POST)
        if restaurant_form.is_valid():
            restaurant = restaurant_form.save()
            return HttpResponseRedirect("/restaurants/all")
        else:
            context['restaurant_form'] = restaurant_form

    if 'restaurant_form' not in context:
        context['restaurant_form'] = RestaurantForm()
    return render_to_response('create.html', RequestContext(request, context))
    

@login_required
def show(request, restaurant_id):
    context = {
        'restaurant': Restaurant.objects.get(pk=restaurant_id)
    }
    
    visit_counter = None
    try:
        visit_counter = RestaurantVisits.objects.get(user=request.user, restaurant=context['restaurant'])
        visit_counter.visit_count += 1
    except Exception as e:
        visit_counter = RestaurantVisits(user=request.user, 
                                         restaurant=context['restaurant'],
                                         visit_count=1)
    
    visit_counter.save()
    context['visit_counter'] = visit_counter

    try:
        RestaurantThumbsDown.objects.get(user=request.user, 
                                         restaurant=context['restaurant'])
        context['thumbsdown'] = True
    except:
        context['thumbsdown'] = False

    context['reviews'] = RestaurantReview.objects.filter(restaurant=context['restaurant'])
    
    return render_to_response('show.html', RequestContext(request, context))


@login_required
def all(request):
    page = request.GET.get('page', None)
    if page is None:
        page = 1

    restaurants = Paginator(Restaurant.objects.all(), 10)


    restaurants = restaurants.page(page)

    context = {
        'restaurants': restaurants,
        'page': page,
    }
    return render_to_response('all.html', RequestContext(request, context))


@login_required
@csrf_exempt
def geocode(request):
    address = urllib.quote_plus(request.GET.get('q'))
    auth_token = "3Nm6yUp4ex3Tp3buS2mpJvA18dfmmc07fQrSeY5h542kWPzW4zPPYcW6bkQyTzamdzVy%2BuYSFKfrBgor2DnLFQ%3D%3D"
    auth_id = "e64dcb80-50a7-47f1-91e4-a376d5e221e1"
    request = "https://api.smartystreets.com/street-address?street=%s&candidates=1&auth-id=%s&auth-token=%s" % ( address, auth_id, auth_token )
    data = simplejson.loads(urllib.urlopen(request).read())
    print data
    return HttpResponse(simplejson.dumps(data))

    
