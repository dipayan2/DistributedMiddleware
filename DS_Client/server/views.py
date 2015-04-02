from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.core.servers.basehttp import FileWrapper

import requests
import time
import os
import csv

import psutil

@csrf_exempt
def index(request):
	if request.method == 'POST':
#		print request.META['HTTP_SAM']
#		print request.body
		for filename, file in request.FILES.iteritems():
			name = request.FILES[filename].name
			print name
		return HttpResponse("Got POST")
	elif request.method == 'GET':

		# psutil calls
		virtualMemory = str(psutil.virtual_memory())
		swapMemory = str(psutil.swap_memory())

		# File to write data for psutil
		filename = "/home/samprit/Desktop/GET_file.txt";

		# Write to file
		fileToSend = open(filename,"w+")
		fileToSend.write(virtualMemory + "\n")
		fileToSend.write(swapMemory + "\n")
		fileToSend.close()

		# Send file as HttpResponse		
		wrapper = FileWrapper(open(filename,"rb"))
		response = HttpResponse(wrapper, content_type='text/plain')
		response['Content-Length'] = os.path.getsize(filename)
		return response

	else:
		raise Http404
		return HttpResponse("failed")
