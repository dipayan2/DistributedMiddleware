from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.core.servers.basehttp import FileWrapper

import requests
import time
import os
import csv

import psutil

from subprocess import Popen, PIPE


#@samprit: while posting finished job, pls send the jobid too
@csrf_exempt
def index(request):

	# dirWhereItWillExec = '/home/samprit/Desktop/DS'
	# dirOfCleintPOSTFile = '/home/samprit/Desktop/DS/Distributed-Systems-Project/'
	dirWhereItWillExec = os.getcwd() + '/'
	dirOfCleintPOSTFile = os.getcwd() + '/'

	if request.method == 'POST':

		# print "fnsdf"
		# IP Address of the requesting POST service
		ipAddrOfPOST = str(request.META['REMOTE_ADDR'])

		# Save the file sent
		for filename, file in request.FILES.iteritems():
			name = request.FILES[filename].name
			fileToSave = request.FILES[filename]
			with open(dirWhereItWillExec + name, 'wb+') as destination:
				for chunk in fileToSave.chunks():
					destination.write(chunk)

		# Iterating through the items
		# for item in request.POST.items():
		# 	print item

		# print "dcamsld"
		# Command to run
		print request.POST
		command = request.POST.__getitem__('Command')
		command = command.replace('+',' ')
		commandList = command.split()
		# print commandList


		# Get Jobid
		jobID = request.POST.__getitem__('Jobid')


		# How to access a list inside querydict
		# print dict(request.POST)['list']


		command = []
		command.append("python")
		command.append("clientPOST.py")
		command.append(dirWhereItWillExec)
		command.append(jobID)
		command.extend(commandList)
		print command

		# Run the process
		process = Popen(command, stdout=PIPE, cwd = dirOfCleintPOSTFile)
		# (output, err) = process.communicate()
		# exit_code = process.wait()

		# print exit_code
		# print output, err, exit_code

		return HttpResponse("File Running")

	elif request.method == 'GET':

		# psutil calls
		print "swapMemory"
		virtualMemory = str(psutil.virtual_memory())
		# swapMemory = str(psutil.swap_memory())

		# co = request.META['HTTP_COMMAND']
		# print co
		# print os.getcwd()

		# File to write data for psutil
		# filename = dirWhereItWillExec + "GET_file.txt";
		filename = dirOfCleintPOSTFile + "GET_file.txt"

		# Write to file
		fileToSend = open(filename,"w+")
		fileToSend.write(virtualMemory)
		# fileToSend.write(swapMemory + "\n")
		fileToSend.close()

		# Send file as HttpResponse		
		wrapper = FileWrapper(open(filename,"rb"))
		response = HttpResponse(wrapper, content_type='text/plain')
		response['Content-Length'] = os.path.getsize(filename)
		return response

	else:
		raise Http404
		return HttpResponse("failed")
