import json

from data import *


# def dict_type():
# 	return [-1,-1,'NA','NA','started','NA']
jobs = {}

def check_user(user,passwd):
	try:
		if(users[user] == passwd):
			return True
		else:
			return False
	except KeyError:
		return False

def add_job(user,jobid,client_id,input_file,command_file,status,output):
	if jobid in jobs.keys():
		return False
	else:
		job = [user,client_id,input_file,command_file,status,output]
		jobs[jobid] = job
		saveAsJson(jobs)
		return True

def update_job(jobid,status,output):
	try:	
		if status == 'complete':
			jobs[jobid][4] = status
			jobs[jobid][5] = output
			saveAsJson(jobs)
			return True
		elif status == 'aborted':
			jobs[jobid][4] = status
			saveAsJson(jobs)
			return True
		else:
			return False
	except KeyError:
		return False

def get_jobs(user):
	try:
		extracted_keys = [k for k, v in jobs.iteritems() if v[0] == user]
		extracted_jobs = []
		for k,v in jobs.iteritems():
			if v[0] == user:
				temp = [k]+v
				extracted_jobs.append(temp)
		return extracted_jobs
	except KeyError:
		return False