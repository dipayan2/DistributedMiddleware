import fcntl
import json
import os

users = {'admin':'admin123'}
ListofIP = ["localhost:8001"]
PrimIP = "10.5.30.143:8001"

MainServerIP = "http://localhost:8000"
SecondaryServerIP = "http://localhost:8001"

# psutilFile = "/home/dipayan/Desktop/Distributed-Systems-Project/psutilFile.json"
# jobFile = "/home/dipayan/Desktop/Distributed-Systems-Project/jobFile.json"
psutilFile = os.getcwd() + "/"
jobFile = os.getcwd() + "/"

def saveAsJson(data, filename):
	if filename == "jobs":
		files = jobFile
	elif filename == "psutil":
		files = psutilFile
	# waiting lock here
	with open(files, 'wb') as fp:
		fcntl.flock(fp, fcntl.LOCK_EX)
		json.dump(data, fp)
		fcntl.flock(fp, fcntl.LOCK_UN)

def loadFromJson(filename):
	if filename == "jobs":
		files = jobFile
	elif filename == "psutil":
		files = psutilFile
	with open(files, 'rb') as fp:
	#waiting lock here
		fcntl.flock(fp, fcntl.LOCK_EX)
		data = json.load(fp)
		fcntl.flock(fp, fcntl.LOCK_UN)
	return data

proxyDict = { 
			"http"  : "", 
			"https" : "", 
			"ftp"   : ""
			}