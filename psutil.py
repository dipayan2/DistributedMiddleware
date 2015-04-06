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


proxyDict = { 
			"http"  : "", 
			"https" : "", 
			"ftp"   : ""
			}


def SendGet():
	# This code will send get requests to all clients
	threading.Timer(10.0,SendGet).start()
	responseArr = {}
	for Ip in ListofIP:
		Addr = "http://"+str(Ip)
		# Addr = "http://localhost:8001"
		r = requests.get(Addr, proxies = proxyDict)
		responseArr[Addr] = r.content


	# with open(psutilFile, "w+") as g:
	# 	fcntl.flock(g, fcntl.LOCK_EX)
	# 	for resp in responseArr:
	# 		g.write(str(resp) + "\n")
	# 	fcntl.flock(g, fcntl.LOCK_UN)

	saveAsJson(responseArr)



def main():
	SendGet()
if __name__ == '__main__':
	main()




#section 1 : Handling Get requests from User

#section 2 : Handling Post request from User

#Section 4 : receiving POST from Client
#Section 5 : sending POST request to Client