import os
import sys
import csv
import simplejson as json
from itertools import chain

dataHeader = [
		"setid",
		"product_code",
		"name",
		"id_root",
		"file_name",
		"date_created",
		"effective_time",
        "product_name",
        "DEA_SCHEDULE_CODE",
        "NDC",
        "DEA_SCHEDULE_NAME",
        "form_code",
        "SPLSIZE",
        "SPLSHAPE",
        "SPLSCORE",
        "SPLCOLOR",
        "SPLIMPRINT",
        "SPL_INGREDIENTS",
        "SPL_INACTIVE_ING",
        "SPLIMAGE",
        "rxcui",
        "rxstring",
        "rxtty",
        "equal_product_code",
        "MARKETING_ACT_CODE"
		]

ingredientsHeader = [
		"product_code",
		"setid",
		"numerator_value",
		"numerator_unit",
		"denominator_value",
		"denominator_unit",
		"base_of_strength"
		]

dataOutput = open('../tmp/processed/csv/spl_data.csv', 'wb')
ingredientsOutput = open('../tmp/processed/csv/spl_ingredients.csv', 'wb')
dataWriter = csv.writer(dataOutput, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
dataWriter.writerow(dataHeader)

ingredientsWriter = csv.writer(ingredientsOutput, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
ingredientsWriter.writerow(ingredientsHeader)

def makeCSV(xmlData):

	for x in xmlData:
		dataRow = []
		for h in dataHeader:
			if h == 'SPL_INACTIVE_ING':
				dataRow.append(";".join(x['data'][h]).rstrip("\n\r ").encode('ascii','ignore'))
			elif h == 'NDC':
				dataRow.append(";".join(x['data'][h]).rstrip("\n\r ").encode('ascii','ignore'))
			elif h == 'SPL_INGREDIENTS':
				dataRow.append(";".join(x['data'][h]).rstrip("\n\r ").encode('ascii','ignore'))
			else:
				dataRow.append(x['data'][h].rstrip("\n\r ").encode('ascii','ignore'))
		dataWriter.writerow(dataRow)
		ingredientsRow = []
		if x['ingredients']:
			for a in x['ingredients']:
				for i in ingredientsHeader:
					idCodes = x['setid_product'].split("-")
					setid = "-".join(idCodes[:-2])
					product_code = idCodes[-2] + "-" + idCodes[-1]
					if i == 'product_code':
						ingredientsRow.append(product_code)
					elif i == 'setid':
						ingredientsRow.append(setid)
					elif i == 'base_of_strength':
						try: 
							ingredientsRow.append(";".join(a['active_moiety_names']).encode('ascii','ignore'))
						except:
							ingredientsRow.append("")
					else:
						try:
							ingredientsRow.append(";".join(a[i]).encode('ascii','ignore'))
						except:
							ingredientsRow.append("")
			ingredientsWriter.writerow(ingredientsRow)


def closeCSV():
	dataOutput.close()
	ingredientsOutput.close()
