import requests
import time
import os
import threading
import json
from data import *
from server_utils import *

class Submit_Jobs(threading.Thread):
	    
	    def __init__(self, job,jobid, clientid):
	    	threading.Thread.__init__(self)
	    	self.job = job     # this job is a list needs different handling
	    	self.clientid = clientid
	    	self.jobid = jobid
	    
	    def run(self):
	    	urlc = "http://"+str(ListofIP[self.clientid])
	    	command = self.job[3]
	    	filename = self.job[2]
	    	payload = {'Command': command , 'Jobid' : self.job[0]}
	    	files = {'file':open(filename,'rb')}
	    	response = 1
	    	r = requests.post(urlc,files = files,data = payload, proxies = proxyDict)
	    	if r.status_code == requests.codes.ok:
	    		response = 1
	    	else:
	    		response = 0
	    	if response == 0:
	    		with open(jobFile,'r+b') as fp:
	    			fcntl.flock(fp,fcntl.LOCK_EX)
	    			jobs = json.load(fp)
	    			jobs[self.jobid][4] = 'failed'
	    			jobs[self.jobid][1] = self.clientid
	    			fcntl.flock(fp,fcntl.LOCK_EX)
	    			url = 'http://'+SecondaryServerIP
	    			r = requests.post(url,data = jobs, proxies= proxyDict)


class Client_Failure(threading.Thread):

	def __init__(self,clientid):
		threading.Thread.__init__(self)
		self.clientid = clientid
	def run(self):
		with open(jobFile, 'r+b') as fp:
			fcntl.flock(fp, fcntl.LOCK_EX) # waiting lock to be added
			jobs = json.load(fp)
			for job in jobs:
				if jobs[job][1] == self.clientid :
					jobs[job][4] = "failed-request"
			fp.seek(0)
			json.dump(jobs, fp)
			fcntl.flock(fp, fcntl.LOCK_UN) # waiting lock to be added



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
			if Client[ListofIP[(LastClientUsed+i)% NoClients]][0] == -1:
				FailedID = (LastClientUsed+ i) % NoClients
				c = Client_Failure(FailedID)
				c.start()
			if Client[(ListofIP[(LastClientUsed+i) % NoClients]][0] > 15 MB:
				LastClientUsed = (LastClientUsed+i) % NoClients
				break
		t = Submit_Jobs(pending_jobs[pendingJobList[0]],pendingJobList[0], LastClientUsed)
		t. start()
		
		del pending_jobs[pendingJobList[0]]
		with open(jobFile,'r+b') as fp:
			fcntl.flock(fp,fcntl.LOCK_EX)
			DwJob = json.load(fp)
			if DwJob[pendingJobList[0]][4] == 'failed-request':
				DwJob[pendingJobList[0]][4] == 'failed'
			else:
				DwJob[pendingJobList[0]][4] == 'started'
				DwJob[pendingJobList[0]][1] = LastClientUsed
			json.dump(DwJob,fp)
			fcntl.flock(fp,fcntl.LOCK_UN)
			url =  'http://'+SecondaryServerIP
			r = requests.post(url,data = DwJob,proxies= proxyDict)
		del pendingJobList[0]
	time.sleep(3)







