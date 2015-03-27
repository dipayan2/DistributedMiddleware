from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import requests
import time
import os


def index(request):	
	if request.method == 'POST':
    		print request
		return HttpResponse("Got POST")
	elif request.method == 'GET':
		print request
		return HttpResponse("Got GET")
	else:
		raise Http404
		return HttpResponse("failed")