from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/', 'accounts.views.login'),
    url(r'^logout/', 'accounts.views.logout'),
    url(r'^new/', 'accounts.views.new'),
    url(r'^edit/', 'accounts.views.edit'),
)
