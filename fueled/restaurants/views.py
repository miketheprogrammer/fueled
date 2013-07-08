# Create your views here.

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import get_current_site
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, NoReverseMatch, resolve
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from restaurants.forms import RestaurantForm
from restaurants.models import Restaurant

@login_required
def create(request):
    context = {}

    if request.method == "POST":
        restaurant_form = RestaurantForm(data=request.POST)
        if restaurant_form.is_valid():
            restaurant = restaurant_form.save()
            return HttpResponse('Restaurant Saved')
        else:
            context['restaurant_form'] = restaurant_form

    if 'restaurant_form' not in context:
        context['restaurant_form'] = RestaurantForm()
    return render_to_response('create.html', RequestContext(request, context))
    

@login_required
def show(request, restaurant_id):
    pass

@login_required
def all(request):
    page = request.GET.get('page', None)
    if page is None:
        page = 1
    restaurants = Paginator(Restaurant.objects.all(), 10)

    if page <= restaurants.num_pages:
        restaurants = restaurants.page(page)

    context = {
        'restaurants': restaurants,
        'page': page,
    }
    return render_to_response('all.html', RequestContext(request, context))
