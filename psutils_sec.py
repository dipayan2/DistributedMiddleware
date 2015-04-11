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
from job_handler_sec import *

run_sec = 0
# need to format the output
def SendGet():
	# This code will send get requests to all clients
	threading.Timer(10.0,SendGet).start()
	responseArr = {}
	if run_sec == 1: 
		# print "run_sec is 1"
		for Ip in getListofIP():
			Addr = "http://"+str(Ip)
			print Addr,
			# Addr = "http://localhost:8001"
			try:
				r = requests.get(Addr, proxies = proxyDict, timeout = connect_timeout)
				mem_data = r.content
				mem = mem_data.split("free=")[1]
				mem = mem.split("L")[0]
				print "    is running"
				responseArr[Addr] = int(mem)
			except Exception, e:
				print e
				responseArr[Addr] = -1
	else:
		# print "waiting for permission"
		pass


	# with open(psutilFile, "w+") as g:
	# 	fcntl.flock(g, fcntl.LOCK_EX)
	# 	for resp in responseArr:
	# 		g.write(str(resp) + "\n")
	# 	fcntl.flock(g, fcntl.LOCK_UN)

	saveAsJson(responseArr,"psutil")

def SendGetPrim():
	headerType = {'FROM': 'Server'}

	t = threading.Timer(10.0,SendGetPrim)
	t.start()
	Addr = "http://"+PrimIP
	print "Checking whether Prime is alive....",
	connect_timeout = 10.0
	try:
		# print "in try"
		r =  requests.get(Addr, proxies = proxyDict, timeout = connect_timeout,headers = headerType)
		responseSec = r.content
		print r.content
	except Exception, e:	
		# print e
		print "Primary server has failed"
		responseSec = "Prim Server failed"
		run_sec = 1
		t.cancel()
		print "Taking over as the Primary Server"
		t1 = threading.Thread(target = handle_jobs_sec)
		t2 = threading.Thread(target = SendGet)
		t1.start()
		t2.start()		


def main():
	SendGetPrim()
	# SendGet()
if __name__ == '__main__':
	main()




#section 1 : Handling Get requests from User

#section 2 : Handling Post request from User

#Section 4 : receiving POST from Client
#Section 5 : sending POST request to Client