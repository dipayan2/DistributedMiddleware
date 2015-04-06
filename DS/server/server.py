#!/usr/bin/python
# DIPAYAN MUKHERJEE
# 11CS30045

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.core.servers.basehttp import FileWrapper

import requests
import time
import os
import csv
import threading

import psutil

from subprocess import Popen, PIPE

ListofIP = []

@csrf_exempt
def SendGet():
	# This code will send get requests to all clients
	threading.Timer(3.0,SendGet).start()
	for Ip in ListofIP:
		Addr = "http://"+str(Ip)
		r = requests.get(Addr)
def main():
	SendGet()
if __name__ == '__main__':
	main()




#section 1 : Handling Get requests from User

#section 2 : Handling Post request from User

#Section 4 : receiving POST from Client
#Section 5 : sending POST request to Client