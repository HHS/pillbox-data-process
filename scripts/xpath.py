#!/usr/bin/python
# ------------------
# Pillbox Xpath script that extracts raw data from XML to yield:
#    1. Rows array, with one row object per product code. 
#    2. Ingredients array, with one object per ingredient
# ------------------
# Requirements: Python 2.6 or greater 

import os, sys, time
import StringIO
from lxml import etree
from itertools import groupby

# Check all XMLs against form codes, discard all XMLs that don't match
codeChecks = [
	"C25158", "C42895", "C42896",
	"C42917", "C42902", "C42904",
	"C42916", "C42928", "C42936",
	"C42954", "C42998", "C42893",
	"C42897", "C60997", "C42905",
	"C42997", "C42910", "C42927",
	"C42931", "C42930", "C61004",
	"C61005", "C42964", "C42963",
	"C42999", "C61006", "C42985",
	"C42992"
	]

print "processing XML with XPATH..."

def parseData(name):

	# Iterparse function that clears the memory each time it finishes running
	def getelements(filename, tag, medicineCheck):
		context = iter(etree.iterparse(filename, events=('start', 'end')))
		_, root = next(context) # get root element
		for event, elem in context:
			# If we pass "yes" via medicineCheck, then we need to return <manufacturedMedicine> instead of <manufacturedProduct> 
			if medicineCheck == 'yes':
				if event == 'end' and elem.tag == "{urn:hl7-org:v3}manufacturedMedicine":
					yield elem
				elif event == 'end' and elem.tag == '{urn:hl7-org:v3}manufacturedProduct' or elem.tag =='manufacturedProduct':
					yield elem
			else:
				if event == 'end' and elem.tag == tag:
					yield elem
		root.clear() # preserve memory

	# ------------------
	# Build SetInfo array
	# ------------------
	setInfo = {}
	setInfo['file_name'] = name
	setInfo['date_created'] = time.strftime("%d/%m/%Y")
	for parent in getelements(name, "{urn:hl7-org:v3}document", 'no'):
		for child in parent.iterchildren('{urn:hl7-org:v3}id'):
			setInfo['id_root'] = child.get('root')
		for child in parent.iterchildren('{urn:hl7-org:v3}setId'):
			setInfo['setid'] = child.get('root')
		for child in parent.iterchildren('{urn:hl7-org:v3}effectiveTime'):
			setInfo['effective_time'] = child.get('value')
		for child in parent.iterchildren('{urn:hl7-org:v3}code'):
			setInfo['document_type'] = child.get('code')

	# --------------------
	# Build Sponsors Array
	# --------------------
	sponsors ={}
	for parent in getelements(name, "{urn:hl7-org:v3}author", 'no'):
		for child in parent.iter('{urn:hl7-org:v3}representedOrganization'):
			for grandChild in child.iterchildren('{urn:hl7-org:v3}name'):
				sponsors['name'] = grandChild.text.strip()
				sponsors['author_type'] = 'labler'
				grandChild.clear()

	for parent in getelements(name, "{urn:hl7-org:v3}legalAuthenticator", 'no'):
		for child in parent.iter('{urn:hl7-org:v3}representedOrganization'):
			for grandChild in child.iterchildren('{urn:hl7-org:v3}name'):
				sponsors['name'] = grandChild.text.strip()
				sponsors['author_type'] = 'legal'
				grandChild.clear()

	# -----------------------------------------
	# Build ProdMedicine and Ingredients arrays
	# -----------------------------------------
	prodMedicines = []
	ingredients = {}
	formCodes = []
	names = []
	# info object, which will later be appended to prodMedicines array
	info = {}
	info['SPLCOLOR']  = []
	info['SPLIMPRINT'] = []
	info['SPLSHAPE'] = []
	info['SPLSIZE'] = []
	info['SPLSCORE']  = []
	info['SPLCOATING']  = []
	info['SPLSYMBOL']  = []
	info['SPLFLAVOR']  = []
	info['SPLIMAGE']  = []
	info['IMAGE_SOURCE'] = []
	info['SPL_INGREDIENTS'] = []
	info['SPL_INACTIVE_ING'] = []
	info['SPL_STRENGTH'] = []
	info['SPLCONTAINS'] = []
	info['APPROVAL_CODE'] = []
	info['MARKETING_ACT_CODE'] = []
	info['DEA_SCHEDULE_CODE'] = []
	info['DEA_SCHEDULE_NAME'] = []
	info['equal_product_code'] = []
	info['NDC'] = []
	info['SPLUSE'] = []

	# substanceCodes will be filled with ingredient codes to check for duplicate ingredients
	substanceCodes = []
	# doses will be filled with ingredient numerator values to check for duplicate ingredients
	doses = []
	# codes stores product_codes, to determine how many unique products \to output with len(codes)
	codes = []
	productCodes = []
	partNumbers = []

	for parent in getelements(name, "{urn:hl7-org:v3}manufacturedProduct", 'yes'):

		equalProdCodes = ''
		# Get equal product code from <definingMaterialKind>
		try:
			equalProdParent = parent.xpath(".//*[local-name() = 'definingMaterialKind']")
			for child in equalProdParent[0].iterchildren():
				if child.get('code') not in equalProdCodes:
					equalProdCodes = child.get('code')
		except:
			equalProdCodes = ''

		def proceed(partCode, partChild, index):
			# There are <manufacturedProduct> elements that have no content and would result
			# in empty objects being appended to ingredients array. So use ingredientTrue to test.
			ingredientTrue = 0

			for child in parent.iterchildren('{urn:hl7-org:v3}name'):
				names.append(child.text.strip())

			for formCode in parent.iterchildren('{urn:hl7-org:v3}formCode'):
				# Only check <manufacturedProduct> level <formCode> against codeChecks if there are no parts
				if partCode == 'zero':
					# Only get product code if form code is in codeChecks
					if formCode.get('code') not in codeChecks:
						# This applies when there are no <parts>, if code not in codeCheck array, pass this <manufacturedProduct> and move
						# onto next  <manufacturedProduct>  
						sys.exit("Not OSDF")
					else:
						for productCode in parent.iterchildren('{urn:hl7-org:v3}code'):
							uniqueCode = productCode.get('code') + '-0'
							formCodes.append(formCode.get('code'))
							# set ingredients array for uniquecode
							ingredients[uniqueCode] = []
							if uniqueCode not in codes:
								codes.append(uniqueCode)
								productCodes.append(productCode.get('code'))
								partNumbers.append('0')
				else:
					# This applies only to <parts>
					for productCode in parent.iterchildren('{urn:hl7-org:v3}code'):
						uniqueCode = productCode.get('code') + '-'+str(index)
						formCodes.append(formCode.get('code'))
						# set ingredients array for uniquecode
						ingredients[uniqueCode] = []
						if uniqueCode not in codes:
							codes.append(uniqueCode)
							productCodes.append(productCode.get('code'))
							partNumbers.append(index)

			# Send code, name and formCode to info = {}
			info['product_code'] = productCodes
			info['part_num'] = partNumbers
			info['product_name'] = names
			info['form_code'] = formCodes

			# Get <containerPackagedProduct> information
			packageProducts = []
			for child in parent.xpath("./*[local-name() = 'asContent']"):
				# Check if we're working with <containerPackagedProduct> or <containerPackagedMedicine>
				checkMedicine =  child.xpath("./*[local-name() = 'containerPackagedMedicine']")
				checkProduct =  child.xpath("./*[local-name() = 'containerPackagedProduct']")
				if len(checkProduct) != 0:
					productType = 'containerPackagedProduct'
				else:
					productType = 'containerPackagedMedicine'
				# Send product
				for grandChild in child.xpath("./*[local-name() = '"+productType+"']"):
					value = grandChild.xpath("./*[local-name() = 'code']")
					# For when there is another <containerPackagedProduct> nested under another <asContent>
					if value[0].get('code') == None:
						subElement = grandChild.xpath(".//*[local-name() = 'asContent']")
						# subValues is an array of all <code> tags under the second instance of <asContent>
						if len(subElement) != 0:
							subValues = subElement[0].xpath(".//*[local-name() = 'code']")
							tempCodes = []
							# Loop through returned values, which come from multiple levels of <containerPackagedProducts>
							for v in subValues:
								if v.get('code') != None:
									packageProducts.append(v.get('code'))
					# Else just print the value from the first <containerPackagedProduct> level
					else:
						packageProducts.append(value[0].get('code'))

			# The getElements() function captures <manufacturedProduct> and </manufacturedProduct>, which is what
			# we're seeing when pacakageProducts has length zero
			if len(packageProducts) != 0:
				info['NDC'].append(packageProducts)


			# Arrays for ingredients
			active = []
			inactive = []
			splStrength = []
			# If partCode is zero, we can find the ingredients directly below the <manufacturedProduct> parent
			# else we need to iterate thorugh the <partProduct> of the <part>, from proceed() function
			if partCode == 'zero':
				level = parent
			else:
				partProduct = partChild.xpath("./*[local-name() = 'partProduct']")
				level = partProduct[0]

			for child in level.iterchildren('{urn:hl7-org:v3}ingredient'):
				# Create temporary object for each ingredient
				ingredientTemp = {}
				ingredientTemp['ingredient_type'] = {}
				ingredientTemp['substance_code'] = {}

				# If statement to find active ingredients
				if child.get('classCode') == 'ACTIB' or child.get('classCode') == 'ACTIM':
					ingredientTrue = 1
					ingredientTemp['active_moiety_names'] = []

					for grandChild in child.iterchildren('{urn:hl7-org:v3}ingredientSubstance'):
						for c in grandChild.iterchildren():
							ingredientTemp['ingredient_type'] = 'active'
							if c.tag == '{urn:hl7-org:v3}name':
								active.append(c.text.strip())
								splStrengthItem = c.text.strip()
								ingredientTemp['substance_name'] = c.text.strip()
							if c.tag == '{urn:hl7-org:v3}code':
								ingredientTemp['substance_code'] = c.get('code')
							if c.tag =='{urn:hl7-org:v3}activeMoiety':
								name = c.xpath(".//*[local-name() = 'name']")
								# Send active moiety to ingredientTemp
								ingredientTemp['active_moiety_names'].append(name[0].text.strip())
					
					for grandChild in child.iterchildren('{urn:hl7-org:v3}quantity'):
						numerator = grandChild.xpath("./*[local-name() = 'numerator']")
						denominator = grandChild.xpath("./*[local-name() = 'denominator']")

						ingredientTemp['numerator_unit'] = numerator[0].get('unit')
						ingredientTemp['numerator_value'] = numerator[0].get('value')
						ingredientTemp['dominator_unit'] = denominator[0].get('unit')
						ingredientTemp['dominator_value'] = denominator[0].get('value')
						splStrengthValue = float(ingredientTemp['numerator_value']) / float(ingredientTemp['dominator_value'])
						splStrengthItem = "%s %s %s" % (splStrengthItem, splStrengthValue, ingredientTemp['numerator_unit'])
						splStrength.append(splStrengthItem)

				# If statement to find inactive ingredients
				if child.get('classCode') == 'IACT':
					ingredientTrue = 1
					# Create object for each inactive ingredient
					for grandChild in child.iterchildren('{urn:hl7-org:v3}ingredientSubstance'):
						for c in grandChild.iterchildren():
							ingredientTemp['ingredient_type'] = 'inactive'
							if c.tag == '{urn:hl7-org:v3}name':
								inactive.append(c.text.strip())
								ingredientTemp['substance_name'] = c.text.strip()
							if c.tag == '{urn:hl7-org:v3}code':
								ingredientTemp['substance_code'] = c.get('code')
				
				ingredients[uniqueCode].append(ingredientTemp)

			# If ingredientTrue was set to 1 above, we know we have ingredient information to append
			if ingredientTrue != 0:
				info['equal_product_code'].append(equalProdCodes)
				info['SPL_INGREDIENTS'].append(active)
				info['SPL_INACTIVE_ING'].append(inactive)
				info['SPL_STRENGTH'].append(splStrength)

			# Second set of child elements in <manufacturedProduct> used for ProdMedicines array
			def checkForValues(type, grandChild):
				value = grandChild.xpath("./*[local-name() = 'value']")
				reference = grandChild.xpath(".//*[local-name() = 'reference']")
				if type == 'SPLIMPRINT':
					value = value[0].text.strip()
				else:
					value = value[0].attrib
				kind = grandChild.find("./{urn:hl7-org:v3}code[@code='"+type+"']")
				if kind !=None:
					if type == 'SPLIMPRINT':
						info[type].append(value)
					elif type == 'SPLSCORE':
						if value.get('value') == None:
							info[type].append('')
						else:
							info[type].append(value.get('code') or value.get('value'))
					elif type == 'SPLIMAGE':
						if reference[0].get('value') == None:
							info[type].append('')
						else:
							splfile = reference[0].get('value').split()
							info[type].append(splfile)
					else:
						info[type].append(value.get('code') or value.get('value'))

			# If partCode is zero, we can find the <asContent> directly below the <manufacturedProduct> parent
			# else we need to iterate thorugh the <partProduct> of the <part>, from proceed() function
			if partCode == 'zero':
				level = parent
			else:
				level = partChild
			for child in level.iterchildren('{urn:hl7-org:v3}subjectOf'):
				 # Get approval code
				try:
					for grandChild in child.findall("{urn:hl7-org:v3}approval"):
						statusCode = grandChild.xpath("./*[local-name() = 'code']")
						info['APPROVAL_CODE'].append(statusCode[0].get('code'))
				except: 
					info['APPROVAL_CODE'].append('')
				#Get marketing act code
				for grandChild in child.findall("{urn:hl7-org:v3}marketingAct"):
					statusCode = grandChild.xpath("./*[local-name() = 'statusCode']")

					info['MARKETING_ACT_CODE'].append(statusCode[0].get('code'))
				# Get policy code
				for grandChild in child.findall("{urn:hl7-org:v3}policy"):
					for each in grandChild.iterchildren('{urn:hl7-org:v3}code'):
						info['DEA_SCHEDULE_CODE'].append(each.get('code'))
						info['DEA_SCHEDULE_NAME'].append(each.get('displayName'))
				for grandChild in child.findall("{urn:hl7-org:v3}characteristic"):
					for each in grandChild.iterchildren('{urn:hl7-org:v3}code'):
						# Run each type through the CheckForValues() function above
						type = each.get('code')
						checkForValues(type, grandChild)
						each.clear()   #clear memory
					grandChild.clear() #clear memory

		# Check if there are <parts> in the manufactured product, if not, partCode = 0
		parts = parent.xpath("./*[local-name() = 'part']")
		if len(parts) == 0:
			# No parts found, so part number is zero, send to proceed() function
			proceed('zero','', '')
		else:
			# Set up an index to pass to proceed() function to determine part number
			index = 1
			for child in parts:
				formCode =  child.xpath(".//*[local-name() = 'formCode']")
				# Check if formCode is in codeChecks
				if formCode[0].get('code') not in codeChecks:
					# If <part> <formCode> is not in codeChecks, move onto next <part>
					pass
				# else send to proceed() function with index
				else:
					proceed(formCode[0].get('code'), child, index)
					index = index + 1

	prodMedicines.append(info)

	prodMedNames = [
					'SPLCOLOR','SPLIMAGE','SPLIMPRINT','product_name','SPLSHAPE',
					'SPL_INGREDIENTS','SPL_INACTIVE_ING','SPLSCORE','SPLSIZE',
					'product_code','part_num','form_code','MARKETING_ACT_CODE',
					'DEA_SCHEDULE_CODE','DEA_SCHEDULE_NAME','NDC','equal_product_code',
					'SPL_STRENGTH'
					]
	setInfoNames = ['file_name','effective_time','id_root','date_created','setid','document_type']
	sponsorNames = ['name','author_type']

	# Loop through prodMedicines as many times as there are unique product codes + part codes combinations, which is len(codes)

	products = []
	if codes: 
		for i in range(0, len(codes)):
			uniqueID = setInfo['id_root'] + '-' + codes[i]
			product = {}
			product['setid_product'] = uniqueID
			product['ndc_codes'] = prodMedicines[0]['NDC'][i]
			tempProduct = {}
			for name in prodMedNames: 
				# Get information at the correct index 
				try:
					if name == 'SPLIMAGE':
						image_file = setInfo['id_root'] + '_' + prodMedicines[0]['product_code'][i] + '_' + prodMedicines[0]['part_num'][i] + '_' + "_".join(prodMedicines[0][name][i])
						tempProduct[name] = image_file
					else:
						tempProduct[name] = prodMedicines[0][name][i]
				except:
					tempProduct[name] = ''
			for name in setInfoNames: 
				tempProduct[name] = setInfo[name]
			for name in sponsorNames: 
				try:
					tempProduct[name] = sponsors[name]
				except:
					tempProduct[name] = ''
			product['data'] = tempProduct
			# Ingredients are showing duplicates again leaving out while fixing.  
			product['ingredients'] = ingredients[codes[i]]
			products.append(product)
		return products
	else:
		sys.exit("Not OSDF")

if __name__ == "__main__":
	test = parseData("../tmp/tmp-unzipped/07374135-f407-4d91-901f-a60fc51f7d9e.xml")
	print test