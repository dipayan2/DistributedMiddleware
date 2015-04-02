from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import requests
import time
import os

from server_utils import *

import psutil

@csrf_exempt
def index(request):

	dirWhereItWillSave = '/home/subham/DS/'

	if request.method == 'POST':
		ipAddrOfPOST = str(request.META['REMOTE_ADDR'])
		
		# Save the file sent
		for filename, file in request.FILES.iteritems():
			name = request.FILES[filename].name
			fileToSave = request.FILES[filename]
			with open(dirWhereItWillSave + name, 'wb+') as destination:
				for chunk in fileToSave.chunks():
					destination.write(chunk)

		#read virtual and swap memories
		fileReceived = open(dirWhereItWillSave + name, "r+")
		virtualMemory, swapMemory = fileReceived.read().split('\n')[0:2]
		fileReceived.close()
		
		return HttpResponse("Got POST")
	elif request.method == 'GET':
		print request
		# return HttpResponse("Dipu is great")
	else:
		raise Http404
		return HttpResponse("failed")
