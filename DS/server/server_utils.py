users = {'admin':'admin123'}

def dict_type():
	return [-1,-1,'started','N/A']

jobs = {}

def check_user(user,passwd):
	try:
		if(users[user] == passwd):
			return True
		else:
			return False
	except KeyError:
		return False

def add_job(user,jobid,client_id,status,output):
	if jobid in jobs.keys():
		return False
	else:
		job = [user,client_id,status,output]
		jobs[jobid] = job
		return True

def update_job(jobid,status,output):
	try:	
		if status == 'complete':
			jobs[jobid][2] = status
			jobs[jobid][3] = output
			return True
		elif status == 'aborted':
			jobs[jobid][2] = status
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