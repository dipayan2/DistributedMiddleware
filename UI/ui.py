import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from data import *
from server_utils import *
sys.path.insert(0,currentdir)

# @csrf_exempt
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import Http404

import requests
import time
import fcntl
import json
import psutil

print os.getcwd()
# username = raw_input("ENTER USERNAME:")
# passwd = raw_input("ENTER PASSWORD:")

# if(check_user(username,passwd)):
# 	print "LOGIN GRANTED"
# else:
# 	print "LOGIN DENIED"
# 	sys.exit()
#connect_timeout = 1.0
username = 'admin'
while True:
	inp = raw_input("ENTER COMMAND: ")
	words = inp.split(" ") # will split the command as well 
	if words[0] == 'run':
		filename = words[1]
		com = inp[len(words[1])+5:]
		url = 'http://'+PrimIP
		payload = {'From':'Web','username':username,'Command':com} 
		# print payload
		files = {'file':open(filename,'rb')}
		print "Sending to url : ", url
		# print com
		# print username
		# print filename
		try:
			r = requests.post(url,files = files,data = payload, proxies= proxyDict)
			print "Successfully sent to primary with jobID : ", r.content
		except Exception, e:
			print "PRIMARY HAS FAILED"
			url = 'http://'+SecondaryServerIP
			try:
				r = requests.post(url,files = files,data = payload, proxies= proxyDict)
				print "Successfully Sent to Secondary Server with jobID : ", r.content
			except Exception, e:
				print "Secondary Server is not reachanble"
				
	elif words[0] == 'status':
		jobid = int(words[1])
		url = 'http://'+PrimIP
		try:
			header = {'From':'Web','USERNAME':username,'JOBID':jobid}			
			r = requests.get(url, proxies = proxyDict, timeout = connect_timeout, headers = header)
			print r.content
		except Exception, e:
			url = 'http://'+SecondaryServerIP
			header = {'From':'Web','USERNAME':username,'JOBID':jobid}
			r = requests.get(url, proxies = proxyDict, timeout = connect_timeout,headers = header)
			print r.content
	else:
		print "WRONG SELECTION...TRY AGAIN"
