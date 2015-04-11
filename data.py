import fcntl
import json
import os

users = {'admin':'admin123'}
ListofIP = ["localhost:8002"]
PrimIP = "localhost:8004"

#MainServerIP = "http://localhost:8004"
SecondaryServerIP = "localhost:8001"

# psutilFile = "/home/dipayan/Desktop/Distributed-Systems-Project/psutilFile.json"
# jobFile = "/home/dipayan/Desktop/Distributed-Systems-Project/jobFile.json"
psutilFile = os.getcwd() + "/psutilFile.json"
jobFile = os.getcwd() + "/jobFile.json"

def saveAsJson(data, filename):
	if filename == "jobs":
		files = jobFile
	elif filename == "psutil":
		files = psutilFile
	# waiting lock here
	print files
	with open(files, 'w+') as fp:
		fcntl.flock(fp, fcntl.LOCK_EX)
		json.dump(data, fp)
		fcntl.flock(fp, fcntl.LOCK_UN)

def loadFromJson(filename):
	try:
		if filename == "psutil":
			files = psutilFile
		elif filename == "jobs":
			files = jobFile
		else:
			files = filename
		print files
		with open(files, 'r+') as fp:
		#waiting lock here
			print "blabla"
			fcntl.flock(fp, fcntl.LOCK_EX)
			data = json.load(fp)
			fcntl.flock(fp, fcntl.LOCK_UN)
		return data
	except Exception, e:
		print e
		return {}
	

proxyDict = { 
			"http"  : "", 
			"https" : "", 
			"ftp"   : ""
			}