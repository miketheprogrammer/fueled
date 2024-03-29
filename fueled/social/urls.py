from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^thumbs/toggle/(?P<restaurant_id>[0-9]*)/$', 'social.views.thumbs_toggle'),
    url(r'^review/add/(?P<restaurant_id>[0-9]*)/$', 'social.views.add_review'),
    url(r'^review/comments/add/(?P<review_id>[0-9]*)/$', 'social.views.add_review_comment'),
    url(r'', 'social.views.team'),
    
)
