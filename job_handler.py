import requests
import time
import os
import threading
from data import *
from server_utils import *
# this function should automatically create a thread but then how to handle the response
# def submit_jobs(job,client_id):
# 	# We should also send the jobId to the user so we can know which job was sent
# 	urlc = "http://"+str(ListofIP[client_id])
# 	command  = job[3]
# 	filename = job[2]
# 	payload = {'Command': command, 'jobid' = job[0]}
# 	files = {'file':open(filename,'rb')}
# 	r = requests.post(url,files = files,data = payload, proxies = proxyDict)
	
# 	#read job json file
# 	# write r back to job files
# 	#write to json file

class Submit_Jobs(threading.Thread):
	    
	    def __init__(self, job, clientid):
	    	threading.Thread.__init__(self)
	    	self.job = job
	    	self.clientid = clientid
	    
	    def run(self):
	    	urlc = "http://"+str(ListofIP[self.clientid])
	    	command = self.job[3]
	    	filename = self.job[2]
	    	payload = {'Command': command , 'Jobid' : self.job[0]}
	    	files = {'file':open(filename,'rb')}
	    	r = requests.post(url,files = files,data = payload, proxies = proxyDict)
	    	#file should be locked
	    	#read jobs from file
	    	#write job back to job dict
	    	# write back to the json file



    
	




LastClientUsed = 0
NoClients = 1 # TO BE CHANGED
# Should constantly loop arouund to find whether there is any pending job and send it to a client
while True:
	jobs = loadFromJson("jobs")
	pending_jobs = {}
	pendingJobList = []
	for job in jobs:
		if jobs[job][4] == 'pending' or jobs[job][4] == 'failed':
			pending_jobs[job] = jobs[job]
			pendingJobList.append(job)
	if any(pending_jobs):
		Client = loadFromJson("psutil")
		for i in xrange(0,NoClients):
			if Client[(ListofIP[(LastClientUsed+i) % NoClients]][0] > 15 MB:
				LastClientUsed = LastClientUsed+i % NoClients
				break
		t = Submit_Jobs(pending_jobs[pendingJobList[0]], LastClientUsed)
		t. start()
		#This modifies the json file of job
		del pending_jobs[pendingJobList[0]]
		jobs[pendingJobList[0]][4] = 'started'
		jobs[pendingJobList[0]][1] = clientid
		del pendingJobList[0]
		saveAsJson(jobs,"jobs")
	time.sleep(3)









# pending_jobs = {}
# ListIP = []
# Client = {} # has the mem space for each client
# pendingJobList = []
# for job in jobs:
# 	if  jobs[job][4] == 'pending' or jobs[job][4] == 'failed':
# 		pending_jobs[job] = jobs[job]
# 		pendingJobList.append(job)
# #check round robin
# for clientid in Client:
# 	if Client[clientid][0] > 15MB:
# 		if submit_jobs(pending_jobs[pendingJobList[0]],clientid) == True:
			# del pending_jobs[pendingJobList[0]]
			# jobs[pendingJobList[0]][4] = 'started'
			# jobs[pendingJobList[0]][1] = clientid
			# del pendingJobList[0]





