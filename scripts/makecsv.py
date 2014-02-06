import os
import sys
import csv
import simplejson as json
from itertools import chain

dataHeader = [
		"setid",
		"product_code",
		"part_num",
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
        "MARKETING_ACT_CODE",
        "author_type",
        "ndc9",
        "SPL_STRENGTH"
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
dataWriter = csv.writer(dataOutput, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
dataWriter.writerow(dataHeader)

ingredientsWriter = csv.writer(ingredientsOutput, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
ingredientsWriter.writerow(ingredientsHeader)

def makeCSV(xmlData):

	for x in xmlData:
		dataRow = []
		for h in dataHeader:
			if h == 'SPL_INACTIVE_ING':
				dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'NDC':
				dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'SPL_INGREDIENTS':
				dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'SPL_STRENGTH':
				dataRow.append(";".join(x['data'][h]).encode('ascii','ignore'))
			elif h == 'part_num':
				dataRow.append(x['data'][h])
			elif h == 'product_name':
				dataRow.append(x['data'][h].encode('ascii','ignore'))
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
									ingredientsRow.append("")
							else:
								try:
									ingredientsRow.append(a[i].encode('ascii','ignore'))
								except:
									ingredientsRow.append("")
						ingredientsWriter.writerow(ingredientsRow)
				except:
					pass


def closeCSV():
	dataOutput.close()
	ingredientsOutput.close()
