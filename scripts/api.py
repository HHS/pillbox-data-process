#!/usr/bin/python

# Import Python Modules 
import os
import sys
import time
import traceback
import csv
import simplejson as json
from datetime import datetime

# Global variables
authorList = []
author = {}

colorList = []
color = {}

def createIndex():

	def authorIndex(data):
		global authorList
		global author

		if data['data']['name'] not in authorList:
			authorList.append(data['data']['name'])
			author[data['data']['name']] = []

		# build author objects
		if data['data']['name'] != "":
			author[data['data']['name']].append(data['setid_product'])

	def colorIndex(data):
		global colorList
		global color

		if data['data']['SPLCOLOR'] not in colorList:
			colorList.append(data['data']['SPLCOLOR'])
			color[data['data']['SPLCOLOR']] = []

		# build color objects 
		# {'C48325': ['3CAF3F19-96B4-DAE6-35AA-05643BD531D2-58177-001']}
		if data['data']['SPLCOLOR'] != "":
			color[data['data']['SPLCOLOR']].append(data['setid_product'])
	
	os.chdir("../tmp/processed/")
	for fn in os.listdir('.'):
		if fn.endswith(".json"):
			data_file = open(fn, "rb").read()
			data = json.loads(data_file)
			authorIndex(data)
			colorIndex(data)

def indexAPI():
	global color
	global author

	authorIndex = []
	for a,n in author.items():
		authorJSON = {
			"author": "",
			"spl-id": [],
			"count": len(n)
			}
		authorJSON['author'] = a
		authorJSON['spl-id'] = n
		authorIndex.append(authorJSON)

	writeIndex(authorIndex, 'author')

	colorIndex = []
	for c,n in color.items():
		colorJSON = {
			"color": "",
			"spl-id": [],
			"count": len(n)
			}		
		colorJSON['color'] = c
		colorJSON['spl-id'] = n
		colorIndex.append(colorJSON)

	writeIndex(colorIndex, 'color')

def writeIndex(output, file_name):
    writeout = json.dumps(output, sort_keys=True, separators=(',',':'))
    f_out = open('../../api/index/%s.json' % file_name, 'wb')
    f_out.writelines(writeout)
    f_out.close()
		
if __name__ == "__main__":
	createIndex()
	indexAPI()