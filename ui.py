import os
from data import *
from server_utils import *

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
import sys, inspect

username = raw_input("ENTER USERNAME:")
passwd = raw_input("ENTER PASSWORD:")

if(check_user(username,passwd)):
	print "LOGIN GRANTED"
else:
	print "LOGIN DENIED"
	sys.exit()

while True:
	inp = raw_input("ENTER COMMAND:")
	words = inp.split(" ")
	if words[0] == 'run':
		filename = words[1]
		url = 'http://'+MainServerIP
		payload = {'From':'Web','username':username,'commmand':words[2]} 
		files = {'file':open(filename,'rb')}
		try:
			r = requests.post(url,files = files,data = payload, proxies= proxyDict)
			print r.content
			flag = 0
		except exception as e:
			flag = 1
			print "PRIMARY HAS FAILED"
		url = 'http://'+SecondaryServerIP
		r = requests.post(url,files = files,data = payload, proxies= proxyDict) 
		if flag == 1:
			print r.content
	elif words[0] == 'status':
		jobid = int(words[1])
		url = 'http://'+MainServerIP
		try:
			r = requests.get(url, proxies = proxyDict, timeout = connect_timeout)
		except exception as e:
			url = 'http://'+SecondaryServerIP
			payload = {'From':'Web','USERNAME':username,'JOBID':jobid}
			r = requests.get(url, proxies = proxyDict, timeout = connect_timeout,data = payload)
			print r.content
	else:
		print "WRONG SELECTION"