# NEED CHANGE MASSIVE

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import requests
import time
import os
import fcntl
import json

from server_utils import *

import psutil

@csrf_exempt

def retrieve_Job():
	dirWhereItWillSave = ''
	#retrieve the filename, command, outputfilename, username
	job = [username, -1, dirWhereItWillSave + filename, command, 'pending', outputfilename]
	return job

def index(request):

	dirWhereItWillSave = '/home/subham/DS/'
	name = 'jobidname.txt'
	jobFile = 'jobFile.json'

	if request.method == 'POST':
		ipAddrOfPOST = str(request.META['REMOTE_ADDR'])
		#save timestamp of post
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
		jobid = 0
		## Function of reading and writing in file
		with open(dirWhereItWillSave+name,'r+') as fp:
			fcntl.flock(fp, fcntl.LOCK_EX) # waiting lock to be implemented
			data = fp.read()
			jobid = int(data)+1
			fp.seek(0)
			fp.write(jobid)
			fcntl.flock(fp,fcntl.LOCK_UN) # waiting lock to be implemented
		job = retrieve_Job()
		with open(dirWhereItWillSave+ jobFile, 'r+b') as fp:
			fcntl.flock(fp, fcntl.LOCK_EX) # waiting lock
			jobs = json.load(fp)
			jobs[jobid] = job
			fp.seek(0)
			json.dump(jobs, fp)
			fcntl.flock(fp,fcntl.LOCK_UN) # waiting lock





		
		return HttpResponse("Got POST")
	elif request.method == 'GET':
		print request
		# return HttpResponse("Dipu is great")
	else:
		raise Http404
		return HttpResponse("failed")
