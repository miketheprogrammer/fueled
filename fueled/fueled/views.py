from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
def home(request):
    if request.user is not None:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard.views.index'))

    return HttpResonseRedirect(reverse('accounts.views.login'))

