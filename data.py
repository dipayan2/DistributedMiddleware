import fcntl
import json

users = {'admin':'admin123'}
ListofIP = ["localhost:8001"]

psutilFile = "/home/dipayan/Desktop/Distributed-Systems-Project/psutilFile.json"
jobFile = "/home/dipayan/Desktop/Distributed-Systems-Project/jobFile.json"

def saveAsJson(data):
	with open(psutilFile, 'wb') as fp:
		fcntl.flock(fp, fcntl.LOCK_EX)
		json.dump(data, fp)
		fcntl.flock(fp, fcntl.LOCK_UN)

def loadFromJson():
	with open(psutilFile, 'rb') as fp:
		fcntl.flock(fp, fcntl.LOCK_EX)
		data = json.load(fp)
		fcntl.flock(fp, fcntl.LOCK_UN)
	return data
