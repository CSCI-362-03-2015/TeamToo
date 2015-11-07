import os
# saves having to write out os.path.abspath each time
from os.path import abspath as ap 
import webbrowser
import subprocess
import pickle
from StringIO import StringIO
from base64 import b64encode
import time
import shutil
import datetime

# Deletes all files in the temp folder before running tests
# Credit to http://glowingpython.blogspot.com/2011/04/how-to-delete-all-files-in-directory.html
# for help with removing files
tempPath = "./temp"
tempContents = os.listdir(tempPath)
for tempFile in tempContents:
	os.remove(tempPath + "/" + tempFile)

# Creates a report name using a timestamp so it will not be overwritten
# when creating a new report
# Credit for formatting timestamp: http://stackoverflow.com/questions/2487109/python-date-time-formatting
# Not used yet
localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
reportName = "results_" + timeString + ".html"	

# This file contains the first part is the HTML styling. Makes things 
# look nice. Also is the top portion of the HTML file.
# note that top.html starts the table header
f = open(ap("./opt/top.html"), "r")
top = f.read()
f.close()

# add date to top
top = top % datetime.datetime.now().strftime("%x at %X")

# Opens results.html, the file where the test results will be written
# and writes the contents of top.html into the file. This includes
# the style and first header for the HTML list (ie: top part).
#f = open(ap("./temp/" + reportName), "w")
f = open(ap("./temp/results.html"), "w")
f.write(top)
f.close()

# lists the 'testCases' directory
testCases = os.listdir(ap("./testCases"))

# list to populate testCase data with
testCasesData = []

for testCase in testCases:
	# dictionary to populate individual test case data with
	testCaseData = {}
	f = open(ap("./testCases/" + testCase), "r")

	# iterate over each line in the test case file, separating the
	# key and values by a colon (:) and stripping any leading/
	# trailing whitespace; then insert into testCaseData
	
	for line in f:
		if line != "" and line != "\n":
			split_line = line.split(":")
			testCaseData[split_line[0].strip()] = split_line[1].strip()
	f.close()

	# insert the individual testCases into their correct location
	# in 'testCasesData' (note the s)
	testCaseIndex = int(testCaseData['test_number'])
	testCasesData.insert(testCaseIndex, testCaseData)
	
# Good old printf debugging (DON'T REMOVE)
# for i, testCase in enumerate(testCasesData):
# 	print "Test %s: " % (i + 1)	
#	for k, v in testCase.iteritems():
#		print "\t%s=%s" % (k,v)

for testCaseData in testCasesData:
	serializedData = StringIO()
	pickle.dump(testCaseData, serializedData)
	os.system("python " + "./testCaseExecutables/testCase" + testCaseData['test_number'] + '.py \'' + b64encode(serializedData.getvalue()) + '\'')
	serializedData.flush()

#os.system("python " + "./testCaseExecutables/" + caseExe)
#f = open(os.path.abspath('./temp/' + reportName), "a")
f = open(os.path.abspath('./temp/results.html'), "a")
f.write("</tbody></table></div></body></html>")      #writes the bottom of the HTML body to the file.#
f.close()

# currently, just copy results for the report run
shutil.copyfile('./temp/results.html', './reports/' + reportName)

#webbrowser.open('file://' + os.path.realpath(os.path.abspath('./temp/' + reportName)))  #opens the HTML file with the default web browser.#
webbrowser.open('file://' + os.path.realpath(os.path.abspath('./temp/results.html')))  #opens the HTML file with the default web browser.#
#http://stackoverflow.com/a/5943706 >> credit for figuring out "os.path.realpath"#
