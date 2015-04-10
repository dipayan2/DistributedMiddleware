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
import sys, inspect

users = {'admin':'admin123'}
ListofIP = ["localhost:8001"]
PrimIP = "10.5.30.143:8001"

MainServerIP = "http://localhost:8000"
SecondaryServerIP = "http://localhost:8001"



# dirWhereItWillSave = '/home/subham/DS/'
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
dirWhereItWillSave = parentdir

def loadFromJson(filename):
	with open(filename, 'rb') as fp:
	#waiting lock here
		fcntl.flock(fp, fcntl.LOCK_EX)
		data = json.load(fp)
		fcntl.flock(fp, fcntl.LOCK_UN)
	return data

def retrieve_Job(username,filename,command):
	# dirWhereItWillSave = ''
	#retrieve the filename, command, outputfilename, username
	job = [username, -1, dirWhereItWillSave + filename, command, 'pending', '']
	return job

@csrf_exempt
def index(request):

	Jname = 'jobidname.txt' #should be created beforehand
	jobFile = 'jobFile.json'

	# here we need to handle different POST whether from client or Web
	if request.method == 'POST':
		From = request.POST.__getitem__('From')
		if From == 'Client':
			Output = request.POST.__getitem__('Output')
			JobStatus = request.POST.__getitem__('JobStatus')
			Jobid = request.POST.__getitem__('Jobid')
			with open(dirWhereItWillSave+jobFile,'r+b') as fp:
    			fcntl.flock(fp,fcntl.LOCK_EX)
    			jobs = json.load(fp)
    			jobs[Jobid][4] = JobStatus
    			jobs[Jobid][5] = Output
    			# jobs[self.][1] = self.clientid
    			fcntl.flock(fp,fcntl.LOCK_EX)
    			url = 'http://'+SecondaryServerIP
    			r = requests.post(url,data = jobs, proxies= proxyDict)
		elif From == 'Web': #for handling web request
			# ipAddrOfPOST = str(request.META['REMOTE_ADDR'])
			#save timestamp of post
			# Save the file sent
			username = request.POST.__getitem__('username')
			Command = request.POST.__getitem__('Command')
			name = ''
			# inputfilename = request.POST.__getitem__('inputfilename')
			for filename, file in request.FILES.iteritems():
				name = request.FILES[filename].name
				fileToSave = request.FILES[filename]
				with open(dirWhereItWillSave + name, 'wb+') as destination:
					for chunk in fileToSave.chunks():
						destination.write(chunk)
			# #read virtual and swap memories
			# fileReceived = open(dirWhereItWillSave + name, "r+")
			# virtualMemory, swapMemory = fileReceived.read().split('\n')[0:2]
			# fileReceived.close()
			jobid = 0
			## Function of reading and writing in file
			with open(dirWhereItWillSave+Jname,'r+') as fp:
				fcntl.flock(fp, fcntl.LOCK_EX) # waiting lock to be implemented
				data = fp.read()
				jobid = int(data)+1
				fp.seek(0)
				fp.write(jobid)
				fcntl.flock(fp,fcntl.LOCK_UN) # waiting lock to be implemented
			job = retrieve_Job(username,name,Command)
			with open(dirWhereItWillSave+ jobFile, 'w+') as fp:
				fcntl.flock(fp, fcntl.LOCK_EX) # waiting lock
				jobs = json.load(fp)
				jobs[jobid] = job
				fp.seek(0)
				json.dump(jobs, fp)
				fcntl.flock(fp,fcntl.LOCK_UN) # waiting lock	
			# wait to send response until job is complete	
			url = 'http://'+SecondaryServerIP
			payload = {'From':'Server','ClientID':-1,'data':job,'Jobid':jobid}
			r = request.POST(url , data = payload, proxies = proxyDict)
			return HttpResponse(jobid) #check 
		elif From == 'Server':
			with open(dirWhereItWillSave+ jobFile, 'w+') as fp:
				jobs = json.load(fp)
				ClientID = int(request.POST.__getitem__['ClientID'])
				if ClientID < 0:
					jobid = int(request.POST.__getitem__['Jobid'])
					jobdata = dict(request.POST)['data']
					jobs[jobid] = jobdata
				else:
					for job in jobs:
						if jobs[job][1] == Clientid and jobs[job][4] == "started" :
						jobs[job][4] = "failed"
				json.dump(jobs,fp)



	elif request.method == 'GET':
		if request.META['HTTP_FROM'] == 'Web':
			username = request.META['HTTP_USERNAME']
			Jobid = request.META['HTTP_JOBID']
			data = loadFromJson(dirWhereItWillSave+jobFile)
			JobStatus = data[Jobid][4]
			Output = data[Jobid][5]
			ClientId = data[Jobid][1]
			if JobStatus == "finished":
				return HttpResponse(str(ClientId)+" : "+str(Output))
			else:
				return HttpResponse(str(ClientId)+" : "+str(JobStatus))
		elif request.META['HTTP_FROM'] == 'Server':
			return HttpResponse("IamOK") 
		else:
		raise Http404
		return HttpResponse("failed")
