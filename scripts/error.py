#!/usr/bin/python

# Import Python Modules 
import os
import sys
import time
import traceback
import simplejson as json
from datetime import datetime

now = datetime.now()

error_count = 0

errorFile = {"updated": now.strftime("%Y-%m-%d %H:%M"), "errors_total": "", "files": []}

def xmlError(fn):
	global error_count
	exc_type, exc_value, exc_traceback = sys.exc_info()
	error = traceback.format_exc().splitlines()
	if error[-1] != "SystemExit: Not OSDF":
		error_count = error_count + 1
		errorPrint = {"file": fn, "error": error}
		errorFile['files'].append(errorPrint)

def errorWrite():
	global error_count
	errorFile['errors_total'] = error_count
	print error_count, "errors"
	writeout = json.dumps(errorFile, sort_keys=True, separators=(',',':'))
	f_out = open('../errors/errors.json', 'wb')
	f_out.writelines(writeout)
	f_out.close()
