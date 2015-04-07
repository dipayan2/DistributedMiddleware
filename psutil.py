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
			r = requests.get(Addr, proxies = proxyDict, timeout = (connect_timeout, read_timeout))
			responseArr[Addr] = r.content
		except requests.exceptions.ConnectTimeout as e:
			responseArr[Addr] = "Client Failed"


	# with open(psutilFile, "w+") as g:
	# 	fcntl.flock(g, fcntl.LOCK_EX)
	# 	for resp in responseArr:
	# 		g.write(str(resp) + "\n")
	# 	fcntl.flock(g, fcntl.LOCK_UN)

	saveAsJson(responseArr,"psutil")



def main():
	SendGet()
if __name__ == '__main__':
	main()




#section 1 : Handling Get requests from User

#section 2 : Handling Post request from User

#Section 4 : receiving POST from Client
#Section 5 : sending POST request to Client