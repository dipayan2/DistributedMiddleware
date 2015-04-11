from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
import server
from server import views

urlpatterns = patterns('',
	# url(r'^$', views.home),
	url(r'', include('server.urls')),
	url(r'^admin/', include(admin.site.urls)),
)