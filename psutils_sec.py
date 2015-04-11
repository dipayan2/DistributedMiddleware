#!/usr/bin/python
# DIPAYAN MUKHERJEE
# 11CS30045
import requests
import time
import os
import threading

import sys
import fcntl
import json

from data import *

# to store the nodes which are not working
connect_timeout = 1.0
read_timeout = 0.05
# need to format the output
def SendGet():
	# This code will send get requests to all clients
	threading.Timer(10.0,SendGet).start()
	responseArr = {}
	for Ip in ListofIP:
		Addr = "http://"+str(Ip)
		# Addr = "http://localhost:8001"
		try:
			r = requests.get(Addr, proxies = proxyDict, timeout = connect_timeout)
			mem_data = r.content
			mem = mem_data.split("free=")[1]
			mem = mem.split("L")[0]
			print "running"
			responseArr[Addr] = int(mem)
		except Exception, e:
			responseArr[Addr] = -1


	# with open(psutilFile, "w+") as g:
	# 	fcntl.flock(g, fcntl.LOCK_EX)
	# 	for resp in responseArr:
	# 		g.write(str(resp) + "\n")
	# 	fcntl.flock(g, fcntl.LOCK_UN)

	saveAsJson(responseArr,"psutil")

def SendGetPrim():
	headerType = {'FROM': 'Server'}

	t = threading.Timer(10.0,SendGet)
	t.start()
	Addr = "http://"+PrimIP
	try:
		r =  requests.get(Addr, proxies = proxyDict, timeout = connect_timeout,params = headerType)
		responseSec = r.content
	except as e:	
		responseSec = "Prim Server failed"
		global run_sec = 1
		t.cancel()
		t1 = threading.Thread(target = handle_jobs_sec)
		t1.start()		


def main():
	SendGetPrim()
	SendGet()
if __name__ == '__main__':
	main()




#section 1 : Handling Get requests from User

#section 2 : Handling Post request from User

#Section 4 : receiving POST from Client
#Section 5 : sending POST request to Client