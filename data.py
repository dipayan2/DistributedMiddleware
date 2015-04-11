import fcntl
import json
import os

import operator

users = {'admin':'admin123'}
# ListofIP = ["10.132.80.139:8000","10.132.80.139:8001", "10.140.150.171:8000", "10.140.150.171:8002"]
PrimIP = "10.102.61.196:8000"

MainServerIP = "http://" + PrimIP
SecondaryServerIP = "10.140.150.171:8000"
# SecondaryServerIP = "http://localhost:7000"

# psutilFile = "/home/dipayan/Desktop/Distributed-Systems-Project/psutilFile.json"
# jobFile = "/home/dipayan/Desktop/Distributed-Systems-Project/jobFile.json"
psutilFile = os.getcwd() + "/psutilFile.json"
jobFile = os.getcwd() + "/jobFile.json"
lockFile = os.getcwd() + "/lockFile.json"
ipAddrFile = os.getcwd() + "/ipAddr.json"
lockFilePS = os.getcwd() + "/lockFilePS.json"

# to store the nodes which are not working
connect_timeout = 1.0
read_timeout = 0.05

def getListofIP():
	data = {}
	try:
		with open(ipAddrFile, 'r+') as fp:
			data = json.load(fp)
	except Exception, e:
		return []

	ListofIPTuple = sorted(data.items(), key=operator.itemgetter(0))

	ListofIP = []
	for (x,y) in ListofIPTuple:
		ListofIP.append(str(y))

	return ListofIP

def saveAsJson(data, filename):
	tempLockFile = ""
	if filename == "jobs":
		files = jobFile
		tempLockFile = lockFile
	elif filename == "psutil":
		files = psutilFile
		tempLockFile = lockFilePS
	# waiting lock here
	# print files
	with open(tempLockFile,'w+') as lf:
		fcntl.flock(lf,fcntl.LOCK_EX)
		with open(files, 'w+') as fp:
			fcntl.flock(fp, fcntl.LOCK_EX)
			json.dump(data, fp)
			fcntl.flock(fp, fcntl.LOCK_UN)
		fcntl.flock(lf,fcntl.LOCK_UN)

def loadFromJson(filename):
	try:
		tempLockFile = lockFile
		if filename == "psutil":
			files = psutilFile
			tempLockFile = lockFilePS
		elif filename == "jobs":
			files = jobFile
			tempLockFile = lockFile
		else:
			files = filename
		# print files
		data = {}
		with open(tempLockFile,'w+') as lf:
			fcntl.flock(lf,fcntl.LOCK_EX)
			with open(files, 'r+') as fp:
				#waiting lock here
				# print "blabla"
				fcntl.flock(fp, fcntl.LOCK_EX)
				data = json.load(fp)
				fcntl.flock(fp, fcntl.LOCK_UN)
			fcntl.flock(lf,fcntl.LOCK_UN)
		return data
	except Exception, e:
		# print e
		return {}
	

proxyDict = { 
			"http"  : "", 
			"https" : "", 
			"ftp"   : ""
			}