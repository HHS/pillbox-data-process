#!/usr/bin/python

# Import Python Modules 
import os
import sys
import time
import traceback
import csv
import simplejson as json
from datetime import datetime
# Import other files
from xpath import parseData
from rxnorm import rxNorm
import error
import makecsv
import Queue
import threading

os.chdir("../tmp/tmp-unzipped/test/")

# for fn in os.listdir('.'):
# 	if fn.endswith(".xml"):
# 		print fn

for folder in os.listdir('.'):
	print folder
	print "-------"
	# os.chdir(folder)
	# for fn in os.listdir('.'):
	# 	if fn.endswith(".xml"):
	# 		print fn
