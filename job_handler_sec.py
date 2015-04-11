import requests
import time
import os
import threading
import json
from data import *
from server_utils import *

class Submit_Jobs(threading.Thread):
	    
	    def __init__(self, job, clientid):
	    	threading.Thread.__init__(self)
	    	self.job = job
	    	self.clientid = clientid
	    
	    def run(self):
	    	urlc = "http://"+str(ListofIP[self.clientid])
	    	command = self.job[3]
	    	filename = self.job[2]
	    	payload = {'Command': command , 'Jobid' : self.jobid}
	    	files = {'file':open(filename,'rb')}
	    	response = 1
	    	r = requests.post(url,files = files,data = payload, proxies = proxyDict)
	    	if r.status_code == requests.code.ok:
	    		response = 1
	    	else:
	    		response = 0
	    	if response == 0:
	    		with open(jobFile,'r+') as fp:
	    			fcntl.flock(fp,fcntl.LOCK_EX)
	    			jobs = json.load(fp)
	    			jobs[self.jobid][4] = 'failed-request'
	    			jobs[self.jobid][1] = self.clientid
	    			fp.truncate()
	    			fp.seek(0)
	    			json.dump(jobs,fp)
	    			fcntl.flock(fp,fcntl.LOCK_UN)



class Client_Failure(threading.Thread):

	def __init__(self,clientid):
		threading.Thread.__init__(self)
		self.clientid = clientid
	def run(self):
		with open(jobFile, 'r+b') as fp:
			fcntl.flock(fp, fcntl.LOCK_EX) # waiting lock to be added
			jobs = json.load(fp)
			for job in jobs:
				if jobs[job][1] == self.clientid and jobs[job][4] == 'started':
					jobs[job][4] = "failed"
			fp.seek(0)
			json.dump(jobs, fp)
			fcntl.flock(fp, fcntl.LOCK_UN) # waiting lock to be added


def handle_jobs_sec():
	LastClientUsed = 0
	NoClients = len(ListofIP)
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
				if Client["http://"+str(ListofIP[(int(LastClientUsed)+int(i))% int(NoClients)])] == -1:
					FailedID = (int(LastClientUsed)+ int(i)) % int(NoClients)
					c = Client_Failure(FailedID)
					c.start()
				if Client["http://"+str(ListofIP[(int(LastClientUsed)+int(i)) % int(NoClients)])] > 15000000:
					LastClientUsed = (int(LastClientUsed)+int(i)) % int(NoClients)
					break
			t = Submit_Jobs(pending_jobs[pendingJobList[0]], LastClientUsed)
			t. start()
			del pending_jobs[pendingJobList[0]]
			with open(jobFile,'r+') as fp:
				fcntl.flock(fp,fcntl.LOCK_EX)
				DwJob = json.load(fp)
				if DwJob[pendingJobList[0]][4] == 'failed-request':
					DwJob[pendingJobList[0]][4] = 'failed'
				else:
					DwJob[pendingJobList[0]][4] = 'started'
					DwJob[pendingJobList[0]][1] = int(LastClientUsed)
				fp.truncate()
				fp.seek(0)
				json.dump(DwJob,fp)
				fcntl.flock(fp,fcntl.LOCK_UN)
			del pendingJobList[0]
		time.sleep(3)







