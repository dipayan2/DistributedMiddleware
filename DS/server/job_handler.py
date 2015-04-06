from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import requests
import time
import os

from server_utils import *
def submit_jobs(job,client_id):
	#send file using POST to client 
	#return True if Ok, otherwise false

pending_jobs = {}
ListIP = []
Client = {} # has the mem space for each client
pendingJobList = []
for job in jobs:
	if  jobs[job][4] == 'pending' or jobs[job][4] == 'failed':
		pending_jobs[job] = jobs[job]
		pendingJobList.append(job)
#check round robin
for clientid in Client:
	if Client[clientid][0] > 15MB:
		if submit_jobs(pending_jobs[pendingJobList[0]],clientid) == True:
			del pending_jobs[pendingJobList[0]]
			jobs[pendingJobList[0]][4] = 'started'
			jobs[pendingJobList[0]][1] = clientid
			del pendingJobList[0]




