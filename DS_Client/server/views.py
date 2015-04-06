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

@csrf_exempt
def index(request):

	dirWhereItWillExec = '/home/dipayan/Desktop/'

	if request.method == 'POST':

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

		# Command to run
		command = request.POST.__getitem__('Command')
		command = command.replace('+',' ')
		commandList = command.split()
		# print commandList

		# Output File where the results will be saved
		# outputFile = request.POST.__getitem__('Output')
		# outputFile = outputFile.replace('+',' ')
		# print outputFile

		# time.sleep(10)

		# Run the process
		process = Popen(commandList, stdout=PIPE, cwd = dirWhereItWillExec)
		(output, err) = process.communicate()
		exit_code = process.wait()

		print exit_code

		return HttpResponse(output)

	elif request.method == 'GET':

		# psutil calls
		virtualMemory = str(psutil.virtual_memory())
		swapMemory = str(psutil.swap_memory())

		# File to write data for psutil
		filename = dirWhereItWillExec + "GET_file.txt";

		# Write to file
		fileToSend = open(filename,"w+")
		fileToSend.write(virtualMemory + "\n")
		fileToSend.write(swapMemory + "\n")
		fileToSend.close()

		# Send file as HttpResponse		
		wrapper = FileWrapper(open(filename,"rb"))
		response = HttpResponse(wrapper, content_type='text/plain')
		response['Content-Length'] = os.path.getsize(filename)
		return response

	else:
		raise Http404
		return HttpResponse("failed")
