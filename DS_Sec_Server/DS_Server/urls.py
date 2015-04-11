from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from DS_Server import views

urlpatterns = patterns('',
	url(r'^$', views.index),
)
