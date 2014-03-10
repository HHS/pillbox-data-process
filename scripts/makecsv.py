import os
import sys
import csv
import simplejson as json
from itertools import chain
import datetime

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d %H:%M")

dataHeader = [
		"setid",
		"file_name",
		"medicine_name",
		"part_medicine_name",
		"product_code",
		"part_num",
		"ndc9",
		"author",
		"author_type",
		"dailymed_date",
		"effective_time",
		"DEA_SCHEDULE_CODE",
		"DEA_SCHEDULE_NAME",
		"MARKETING_ACT_CODE",
		"NDC",
		"SPLCOLOR",
		"SPLIMAGE",
		"SPLIMPRINT",
		"SPLSCORE",
		"SPLSHAPE",
		"SPLSIZE",
		"SPL_INACTIVE_ING",
		"SPL_INGREDIENTS",
		"SPL_STRENGTH",
		"document_type",
		"dosage_code",
		"rxcui",
		"rxstring",
		"rxtty",
		"source",
		"equal_product_code"
		]

ingredientsHeader = [
		"product_code",
		"setid",
		"part_num",
		"numerator_value",
		"numerator_unit",
		"denominator_value",
		"denominator_unit",
		"base_of_strength"
		]

dataOutput = open('../tmp/processed/csv/spl_data.csv', 'wb')
ingredientsOutput = open('../tmp/processed/csv/spl_ingredients.csv', 'wb')
dataWriter = csv.writer(dataOutput, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
dataWriter.writerow(dataHeader)

ingredientsWriter = csv.writer(ingredientsOutput, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
ingredientsWriter.writerow(ingredientsHeader)

def makeCSV(xmlData):

	for x in xmlData:
		dataRow = []
		for h in dataHeader:
			if h == 'SPL_INACTIVE_ING':
				if x['data'][h] == None:
					dataRow.append(x['data'][h])
				else:
					dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'NDC':
				dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'SPL_INGREDIENTS':
				if x['data'][h] == None:
					dataRow.append(x['data'][h])
				else:
					dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'SPL_STRENGTH':
				if x['data'][h] == None:
					dataRow.append(x['data'][h])
				else:
					dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'part_num':
				dataRow.append(x['data'][h])
			elif h == 'product_name':
				dataRow.append(x['data'][h].encode('ascii','ignore'))
			else:
				if x['data'][h] == None:
					dataRow.append(x['data'][h])
				else:
					dataRow.append(x['data'][h].encode('ascii','ignore'))
		dataWriter.writerow(dataRow)
		if x['ingredients']:
			for a in x['ingredients']:
				try:
					if a['active_moiety_names']:
						ingredientsRow = []
						for i in ingredientsHeader:
							idCodes = x['setid_product'].split("-")
							setid = "-".join(idCodes[:-3])
							product_code = idCodes[-3] + "-" + idCodes[-2]
							part_num = idCodes[-1]
							if i == 'product_code':
								ingredientsRow.append(product_code)
							elif i == 'setid':
								ingredientsRow.append(setid)
							elif i == 'part_num':
								ingredientsRow.append(part_num)
							elif i == 'base_of_strength':
								try:
									ingredientsRow.append(";".join(a['active_moiety_names']).encode('ascii','ignore'))
								except:
									ingredientsRow.append(None)
							else:
								try:
									ingredientsRow.append(a[i].encode('ascii','ignore'))
								except:
									ingredientsRow.append(None)
						ingredientsWriter.writerow(ingredientsRow)
				except:
					pass

def closeCSV():
	dataOutput.close()
	ingredientsOutput.close()

def makeDataPackage():
	datapackage = {
				  "name": "pillbox",
				  "title": "Pillbox SPL Data",
				  "date_updated": today,
				  "resources": [
				    {
						"path": "spl_data.csv",
						"schema": {
						"fields": [
						  {"name": "setid","type": "string"},
						  {"name": "file_name","type": "string"},
						  {"name": "medicine_name","type": "string"},
						  {"name": "product_code","type": "string"},
						  {"name": "part_num","type": "integer"},
						  {"name": "ndc9","type": "string"},
						  {"name": "author","type": "string"},
						  {"name": "author_type","type": "string"},
						  {"name": "date_created","type": "string"},
						  {"name": "effective_time","type": "integer"},
						  {"name": "DEA_SCHEDULE_CODE","type": "string"},
						  {"name": "DEA_SCHEDULE_NAME","type": "string"},
						  {"name": "MARKETING_ACT_CODE","type": "string"},
						  {"name": "NDC","type": "string"},
						  {"name": "SPLCOLOR","type": "string"},
						  {"name": "SPLIMAGE","type": "string"},
						  {"name": "SPLIMPRINT","type": "string"},
						  {"name": "SPLCOLOR","type": "string"},
						  {"name": "SPLSCORE","type": "integer"},
						  {"name": "SPLSHAPE","type": "string"},
						  {"name": "SPLSIZE","type": "integer"},
						  {"name": "SPL_INACTIVE_ING","type": "string"},
						  {"name": "SPL_INGREDIENTS","type": "string"},
						  {"name": "SPL_STRENGTH","type": "string"},
						  {"name": "SPLSHAPE","type": "string"},
						  {"name": "document_type","type": "string"},
						  {"name": "dosage_code","type": "string"},
						  {"name": "rxcui","type": "string"},
						  {"name": "rxstring","type": "string"},
						  {"name": "rxtty","type": "string"},
						  {"name": "source","type": "string"},
						  {"name": "equal_product_code","type": "string"}
						]
						}
				    },
					{
						"path": "spl_ingredients.csv",
						"schema": {
							"fields": [
							{"name": "product_code","type": "string"},
							{"name": "setid","type": "string"},
							{"name": "part_num","type": "string"},
							{"name": "numerator_value","type": "string"},
							{"name": "numerator_unit","type": "string"},
							{"name": "denominator_value","type": "string"},
							{"name": "denominator_unit","type": "string"},
							{"name": "base_of_strength","type": "string"}
							]
						}
					}
				  ]
				}

	writeout = json.dumps(datapackage, sort_keys=True, separators=(',',':'), indent=4 * ' ')
	f_out = open('../../../api/datapackage.json', 'wb')
	f_out.writelines(writeout)
	f_out.close()
	print "Datapackage.json created..."
