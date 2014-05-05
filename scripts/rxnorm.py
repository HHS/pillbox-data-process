#!/usr/bin/python
import os
import sys
import requests
import simplejson as json

def connectionCheck():
	url = 'http://rxnav.nlm.nih.gov/REST/version'
	header = {'Accept': 'application/json'}
	getCheck = requests.get(url, headers=header)
	if getCheck.status_code != requests.codes.ok:
		response = "RXNorm server response error. Response code: %s" % getCheck.status_code
	else:
		response = "Connection check complete. RXNorm online. Response code: %s" % getCheck.status_code
	return response

def rxNorm(ndc):
	# ndc value coming from master.py
	# ndc = [array of ndc values]
	if ndc[0] is None:
		return {"rxcui": "", "rxtty": "", "rxstring": ""}
	else:
		# if internet or request throws an error, print out to check connection and exit
		try:
			baseurl = 'http://rxnav.nlm.nih.gov/REST/'

			# Searching RXNorm API, Search by identifier to find RxNorm concepts
			# http://rxnav.nlm.nih.gov/REST/rxcui?idtype=NDC&id=0591-2234-10
			# Set url parameters for searching RXNorm for SETID
			ndcSearch = 'rxcui?idtype=NDC&id='

			# Search RXNorm API, Return all properties for a concept
			rxPropSearch = 'rxcui/'
			rxttySearch = '/property?propName=TTY'
			rxstringSearch = '/property?propName=RxNorm%20Name'

			# Request RXNorm API to return json
			header = {'Accept': 'application/json'}
			def getTTY(rxCUI):
				# Search RXNorm again using RXCUI to return RXTTY & RXSTRING
				getTTY = requests.get(baseurl+rxPropSearch+rxCUI+rxttySearch, headers=header)

				ttyJSON = json.loads(getTTY.text, encoding="utf-8")

				return ttyJSON['propConceptGroup']['propConcept'][0]['propValue']

			def getSTRING(rxCUI):
				# Search RXNorm again using RXCUI to return RXTTY & RXSTRING
				getString = requests.get(baseurl+rxPropSearch+rxCUI+rxstringSearch, headers=header)
				stringJSON = json.loads(getString.text, encoding="utf-8")

				return stringJSON['propConceptGroup']['propConcept'][0]['propValue']

			# Search RXNorm using NDC code, return RXCUI id
			# ndc = [ndc1, ndc2, ... ]
			for item in ndc:
				getRXCUI = requests.get(baseurl+ndcSearch+item, headers=header)
				if getRXCUI.status_code != requests.codes.ok:
					print "RXNorm server response error. Response code: %s" % getRXCUI.status_code
				rxcuiJSON = json.loads(getRXCUI.text, encoding="utf-8")
				# Check if first value in list returns a RXCUI, if not go to next value
				try:
					if rxcuiJSON['idGroup']['rxnormId']:
						rxCUI = rxcuiJSON['idGroup']['rxnormId'][0]
						rxTTY = getTTY(rxCUI)
						rxSTRING = getSTRING(rxCUI)
						return {"rxcui": rxCUI, "rxtty": rxTTY, "rxstring": rxSTRING}
				except:
					# if last item return null values
					if item == ndc[-1]:
						return {"rxcui": "", "rxtty": "", "rxstring": ""}
					pass
		except:
			sys.exit("RXNorm connection")

if __name__ == "__main__":
	# Test with sample NDC codes, one works, one doesn't
	dataTest = rxNorm(['66435-101-42', '66435-101-56', '66435-101-70', '66435-101-84', '66435-101-14', '66435-101-16', '66435-101-18'])
	print dataTest
