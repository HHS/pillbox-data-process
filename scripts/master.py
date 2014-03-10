#!/usr/bin/python

# Import Python Modules
import os
import sys
import time
import traceback
import csv
import glob
import simplejson as json
from datetime import datetime
# Import other files
from xpath import parseData
from rxnorm import rxNorm
import error
import makecsv
import Queue
import threading


master_t0 = time.time()

# Global variables
masterList = []
file_count = 0

os.chdir("../tmp/tmp-unzipped/")

queue = Queue.Queue()

def xmlProcess(fn):
	global file_count
	try:
		file_count = file_count + 1
		# run xpath.py on each file
		xmlData = parseData(fn)

		for x in xmlData:
			rxnormData = rxNorm(x['ndc_codes'])
			x['data']['rxcui'] = rxnormData['rxcui']
			x['data']['rxtty'] = rxnormData['rxtty']
			x['data']['rxstring'] = rxnormData['rxstring']
			try:
				ndc9 = x['data']['product_code'].split("-")
				if len(ndc9[0]) < 5:
					ndc9[0] = "0%s" % ndc9[0]
				if len(ndc9[1]) < 4:
					ndc9[1] = "0%s" % ndc9[1]
				x['data']['ndc9'] = "".join(ndc9)
			except:
				x['data']['ndc9'] = ""
		# Make indidivdual json files per SETID-NDC code
			writeout = json.dumps(x, sort_keys=True, separators=(',',':'))
			f_out = open('../processed/json/%s.json' % x['setid_product'], 'wb')
			f_out.writelines(writeout)
			f_out.close()
		# Make CSV file for output, one row per SETID-NDC code
		makecsv.makeCSV(xmlData)
	except:
		error.xmlError(fn)

class ThreadXML(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			#grabs file from queue
			fn = self.queue.get()
			#grabs file and processes
			xmlProcess(fn)

			#signals to queue job is done
			self.queue.task_done()

def main():
	#spawn a pool of threads, and pass them queue instance
	for i in range(20):
		t = ThreadXML(queue)
		t.setDaemon(True)
		t.start()

	#populate queue with data
	for d in os.listdir('.'):
		files = glob.glob('%s/*.xml' % d)
		for fn in files:
			queue.put(fn)
	#wait on the queue until everything has been processed
	queue.join()

main()

# Calculate the total time and print to console.
master_t1 = time.time()
total_time = (master_t1-master_t0)/60
print file_count, "XML files processed"
error.errorWrite()
makecsv.closeCSV()
makecsv.makeDataPackage()
print "Processing complete. Total Processing time = %d minutes" % total_time
