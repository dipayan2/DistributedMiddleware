from data import *
import sys
import time
import requests

from subprocess import Popen, PIPE


# Run the file and send a POST
def runFile(dirWhereItWillExec, commandList):
	process = Popen(commandList, stdout=PIPE, cwd = dirWhereItWillExec)
	(output, err) = process.communicate()
	exit_code = process.wait()

	print output
	
	
	# There will be two fields in the POST data
	# One is 'From' which tells whether the POST is from Client or UI
	# The other is 'Output' which has the output data
	dataToSend = {}
	dataToSend['From'] = 'Client'
	dataToSend['Output'] = output
	dataToSend['JobStatus'] = 'finished'

	# Send POST
	# headerType = {'content-type': 'application/x-www-form-urlencoded'}

	try:
		r = requests.post(MainServerIP, data = dataToSend, proxies = proxyDict)
	except Exception, e:
		print "Main Server Failed"
		try:
			r = requests.post(SecondaryServerIP, data = dataToSend, proxies = proxyDict)
		except Exception, e:
			print "Both Servers Failed...System Critical"



# Takes input from the commandLine
# First argument is the directory where the file is stored
# Rest of the arguments specify how to run the file
def main():

	dirWhereItWillExec = sys.argv[1]
	commandList = []

	for arg in xrange(2,len(sys.argv)):
		commandList.append(sys.argv[arg])

	runFile(dirWhereItWillExec, commandList)


if __name__ == '__main__':
	main()