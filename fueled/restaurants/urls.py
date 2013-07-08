from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^(?P<restaurant_id>[0-9]*)/$', 'restaurants.views.show'),
    url(r'^create/$', 'restaurants.views.create'),
)
