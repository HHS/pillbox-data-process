#!/usr/bin/python
# ------------------
# Pillbox Xpath script that extracts raw data from XML to yield:
#    1. Rows array, with one row object per product code.
#    2. Ingredients array, with one object per ingredient
# ------------------
# Requirements: Python 2.6 or greater

import os, sys, time
import StringIO
import atexit
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
		context = iter(etree.iterparse(filename))
		_, root = next(context) # get root element
		for event, elem in context:
			# if event == 'start':
				# If we pass "yes" via medicineCheck, then we need to return <manufacturedMedicine> instead of <manufacturedProduct>
				if medicineCheck == 'yes':
					if elem.tag == "{urn:hl7-org:v3}manufacturedMedicine":
						yield elem
					elif elem.tag == '{urn:hl7-org:v3}manufacturedProduct' or elem.tag =='manufacturedProduct':
						yield elem
				else:
					if tag.find('{') >= 0:
						tag = tag[16:]
					if elem.tag.find('{') >= 0:
						elem.tag = elem.tag[16:]

					if elem.tag == tag:
						yield elem
		root.clear() # preserve memory

	# ------------------
	# Build SetInfo array
	# ------------------
	setInfo = {}
	filename = name.split('/')
	setInfo['file_name'] = filename[1]
	setInfo['source'] = filename[0]
	setInfo['dailymed_date'] = time.strftime("%d/%m/%Y")

	def getInfo():
		# Get information at parent level
		tree = etree.parse(name)
		root = tree.getroot()
		for child in root.xpath("./*[local-name() = 'id']"):
			setInfo['id_root'] = child.get('root')
		for child in root.xpath("./*[local-name() = 'setId']"):
			setInfo['setid'] = child.get('root')
		for child in root.xpath("./*[local-name() = 'effectiveTime']"):
			setInfo['effective_time'] = child.get('value')
		for child in root.xpath("./*[local-name() = 'code']"):
			setInfo['document_type'] = child.get('code')

	# --------------------
	# Build Sponsors Array
	# --------------------
	sponsors = {}
	for parent in getelements(name, "{urn:hl7-org:v3}author", 'no'):
		for child in parent.xpath(".//*[local-name() = 'representedOrganization']"):
			for grandChild in child.xpath("./*[local-name() = 'name']"):
				sponsors['author'] = grandChild.text.strip()
				sponsors['author_type'] = 'labler'
				grandChild.clear()

	for parent in getelements(name, "{urn:hl7-org:v3}legalAuthenticator", 'no'):
		for child in parent.xpath(".//*[local-name() = 'representedOrganization']"):
			for grandChild in child.xpath("./*[local-name() = 'representedOrganization']"):
				sponsors['author'] = grandChild.text.strip()
				sponsors['author_type'] = 'legal'
				grandChild.clear()

	# -----------------------------------------
	# Build ProdMedicine and Ingredients arrays
	# -----------------------------------------
	prodMedicines = []
	ingredients = {}
	formCodes = []
	names = []
	partnames = []
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

		def proceed(partCode, partChild, index):
			equalProdCodes = ''
			# There are <manufacturedProduct> elements that have no content and would result
			# in empty objects being appended to ingredients array. So use ingredientTrue to test.
			ingredientTrue = 0

			# Get equal product code from <definingMaterialKind>
			try:
				equalProdParent = parent.xpath(".//*[local-name() = 'definingMaterialKind']")

				code = equalProdParent[0].xpath("./*[local-name() = 'code']")
				if code[0].get('code') not in equalProdCodes:
					equalProdCodes = code[0].get('code')
			except:
				equalProdCodes = ''

			if partCode == 'zero':
				getInfo()
				for productCode in parent.xpath("./*[local-name() = 'code']"):
					uniqueCode = productCode.get('code') + '-0'
					# set ingredients array for uniquecode
					ingredients[uniqueCode] = []
					if uniqueCode not in codes:
						codes.append(uniqueCode)
						productCodes.append(productCode.get('code'))
						partNumbers.append('0')
			else:
				# This applies only to <parts>
				for productCode in parent.xpath("./*[local-name() = 'code']"):
					uniqueCode = productCode.get('code') + '-'+str(index)
					formCodes.append(partCode)
					# set ingredients array for uniquecode
					ingredients[uniqueCode] = []
					if uniqueCode not in codes:
						codes.append(uniqueCode)
						productCodes.append(productCode.get('code'))
						partNumbers.append(index)

			# Get <containerPackagedProduct> information
			packageProducts = []
			for child in parent.xpath("./*[local-name() = 'asContent']"):
				# Check if we're working with <containerPackagedProduct> or <containerPackagedMedicine>
				checkMedicine =  child.xpath("./*[local-name() = 'containerPackagedMedicine']")
				checkProduct =  child.xpath("./*[local-name() = 'containerPackagedProduct']")
				if checkProduct:
					productType = 'containerPackagedProduct'
				else:
					productType = 'containerPackagedMedicine'
				# Send product
				for grandChild in child.xpath("./*[local-name() = '"+productType+"']"):
					value = grandChild.xpath("./*[local-name() = 'code']")
					form = grandChild.xpath("./*[local-name() = 'formCode']")
					# For when there is another <containerPackagedProduct> nested under another <asContent>
					if value[0].get('code') == None:
						subElement = grandChild.xpath(".//*[local-name() = 'asContent']")
						# subValues is an array of all <code> tags under the second instance of <asContent>
						if subElement:
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
			if packageProducts:
				info['NDC'].append(packageProducts)

			# Arrays for ingredients
			active = []
			inactive = []
			splStrength = []
			# If partCode is zero, we can find the ingredients directly below the <manufacturedProduct> parent
			# else we need to iterate thorugh the <partProduct> of the <part>, from proceed() function

			if partCode == 'zero':
				level = parent
				for child in parent.xpath("./*[local-name() = 'name']"):
					names.append(child.text.strip())
					partnames.append('')
			else:
				for child in parent.iterchildren('{urn:hl7-org:v3}name'):
					names.append(child.text.strip())

				partProduct = partChild.xpath("./*[local-name() = 'partProduct']")
				if not partProduct:
					partProduct = partChild.xpath("./*[local-name() = 'partMedicine']")

				level = partProduct[0]
				for child in partProduct[0].xpath("./*[local-name() = 'name']"):
					partnames.append(child.text.strip())
			for child in level.xpath("./*[local-name() = 'ingredient']"):
				# Create temporary object for each ingredient
				ingredientTemp = {}
				ingredientTemp['ingredient_type'] = {}
				ingredientTemp['substance_code'] = {}

				# If statement to find active ingredients
				if child.get('classCode') == 'ACTIB' or child.get('classCode') == 'ACTIM':
					ingredientTrue = 1
					ingredientTemp['active_moiety_names'] = []

					for grandChild in child.xpath("./*[local-name() = 'ingredientSubstance']"):
						for c in grandChild.iterchildren():
							ingredientTemp['ingredient_type'] = 'active'
							if c.tag == '{urn:hl7-org:v3}name' or c.tag == 'name':
								active.append(c.text.strip())
								splStrengthItem = c.text.strip()
								ingredientTemp['substance_name'] = c.text.strip()
							if c.tag == '{urn:hl7-org:v3}code' or c.tag == 'code':
								ingredientTemp['substance_code'] = c.get('code')
							if c.tag =='{urn:hl7-org:v3}activeMoiety' or c.tag == 'activeMoiety':
								name = c.xpath(".//*[local-name() = 'name']")

								# Send active moiety to ingredientTemp
								try:
									ingredientTemp['active_moiety_names'].append(name[0].text.strip())
								except:
									ingredientTemp['active_moiety_names'].append('')

					for grandChild in child.xpath("./*[local-name() = 'quantity']"):
						numerator = grandChild.xpath("./*[local-name() = 'numerator']")
						denominator = grandChild.xpath("./*[local-name() = 'denominator']")

						ingredientTemp['numerator_unit'] = numerator[0].get('unit')
						ingredientTemp['numerator_value'] = numerator[0].get('value')
						ingredientTemp['dominator_unit'] = denominator[0].get('unit')
						ingredientTemp['dominator_value'] = denominator[0].get('value')
						splStrengthValue = float(ingredientTemp['numerator_value']) / float(ingredientTemp['dominator_value'])
						if str(splStrengthValue)[-1] == '0':
							splStrengthValue = int(splStrengthValue)
						splStrengthItem = "%s %s %s" % (splStrengthItem, splStrengthValue, ingredientTemp['numerator_unit'])
						splStrength.append(splStrengthItem)

				# If statement to find inactive ingredients
				if child.get('classCode') == 'IACT':
					ingredientTrue = 1
					# Create object for each inactive ingredient
					for grandChild in child.xpath("./*[local-name() = 'ingredientSubstance']"):
						for c in grandChild.iterchildren():
							ingredientTemp['ingredient_type'] = 'inactive'
							if c.tag == '{urn:hl7-org:v3}name' or c.tag =='name':
								inactive.append(c.text.strip())
								ingredientTemp['substance_name'] = c.text.strip()
							if c.tag == '{urn:hl7-org:v3}code' or c.tag == 'code':
								ingredientTemp['substance_code'] = c.get('code')
				try:
					ingredients[uniqueCode].append(ingredientTemp)
				except:
					# this is passed because of no uniqeCode assigned when not OSDF
					continue

			# For XML files that have different ingredient element syntax
			# check for inactive ingredients
			for child in level.xpath("./*[local-name() = 'inactiveIngredient']"):
				# Create temporary object for each ingredient
				ingredientTemp = {}
				ingredientTemp['ingredient_type'] = {}
				ingredientTemp['substance_code'] = {}
				ingredientTrue = 1

				for grandChild in child.xpath("./*[local-name() = 'inactiveIngredientSubstance']"):
					for c in grandChild.iterchildren():
						ingredientTemp['ingredient_type'] = 'inactive'
						if c.tag == '{urn:hl7-org:v3}name' or c.tag =='name':
							inactive.append(c.text.strip())
							ingredientTemp['substance_name'] = c.text.strip()
						if c.tag == '{urn:hl7-org:v3}code' or c.tag == 'code':
							ingredientTemp['substance_code'] = c.get('code')
				try:
					ingredients[uniqueCode].append(ingredientTemp)
				except:
					# this is passed because of no uniqeCode assigned when not OSDF
					continue

			# For XML files that have different ingredient element syntax
			# check for active ingredients
			for child in level.xpath("./*[local-name() = 'activeIngredient']"):
				ingredientTemp = {}
				ingredientTemp['ingredient_type'] = {}
				ingredientTemp['substance_code'] = {}
				ingredientTemp['active_moiety_names'] = []
				ingredientTrue = 1

				for grandChild in child.xpath("./*[local-name() = 'activeIngredientSubstance']"):
					for c in grandChild.iterchildren():
						ingredientTemp['ingredient_type'] = 'active'
						if c.tag == '{urn:hl7-org:v3}name' or c.tag == 'name':
							active.append(c.text.strip())
							splStrengthItem = c.text.strip()
							ingredientTemp['substance_name'] = c.text.strip()
						if c.tag == '{urn:hl7-org:v3}code' or c.tag == 'code':
							ingredientTemp['substance_code'] = c.get('code')
						if c.tag =='{urn:hl7-org:v3}activeMoiety' or c.tag == 'activeMoiety':
							name = c.xpath(".//*[local-name() = 'name']")

							# Send active moiety to ingredientTemp
							try:
								ingredientTemp['active_moiety_names'].append(name[0].text.strip())
							except:
								ingredientTemp['active_moiety_names'].append('')

				for grandChild in child.xpath("./*[local-name() = 'quantity']"):
					numerator = grandChild.xpath("./*[local-name() = 'numerator']")
					denominator = grandChild.xpath("./*[local-name() = 'denominator']")

					ingredientTemp['numerator_unit'] = numerator[0].get('unit')
					ingredientTemp['numerator_value'] = numerator[0].get('value')
					ingredientTemp['dominator_unit'] = denominator[0].get('unit')
					ingredientTemp['dominator_value'] = denominator[0].get('value')
					splStrengthValue = float(ingredientTemp['numerator_value']) / float(ingredientTemp['dominator_value'])
					if str(splStrengthValue)[-1] == '0':
						splStrengthValue = int(splStrengthValue)
					splStrengthItem = "%s %s %s" % (splStrengthItem, splStrengthValue, ingredientTemp['numerator_unit'])
					splStrength.append(splStrengthItem)

			# Send code, name and formCode to info = {}
			info['product_code'] = productCodes
			info['part_num'] = partNumbers
			info['medicine_name'] = names
			info['part_medicine_name'] = partnames
			info['dosage_code'] = formCodes
			# If ingredientTrue was set to 1 above, we know we have ingredient information to append
			if ingredientTrue != 0:
				info['equal_product_code'].append(equalProdCodes)
				info['SPL_INGREDIENTS'].append(active)
				info['SPL_INACTIVE_ING'].append(inactive)
				info['SPL_STRENGTH'].append(splStrength)

			# Second set of child elements in <manufacturedProduct> used for ProdMedicines array
			def checkForValues(ctype, grandChild, dup, idx):
				value = grandChild.xpath("./*[local-name() = 'value']")
				reference = grandChild.xpath(".//*[local-name() = 'reference']")
				if ctype == 'SPLIMPRINT':
					value = value[0].text.strip()
				else:
					value = value[0].attrib
				kind = grandChild.find("./{urn:hl7-org:v3}code[@code='"+ctype+"']")
				if kind == None:
					kind = grandChild.find("./code[@code='"+ctype+"']")
				if kind !=None:
					if ctype == 'SPLCOLOR':
						if dup == '1':
							color1 = info[ctype][idx]
							if value.get('code') == None:
								color2 = ''
							else:
								color2 = value.get('code')
							info[ctype][idx] = "%s;%s" % (color1,color2)
						else:
							info[ctype].append(value.get('code'))
					elif ctype == 'SPLIMPRINT':
						info[ctype].append(value)
					elif ctype == 'SPLSCORE':
						if value.get('value') == None:
							info[ctype].append('')
						else:
							info[ctype].append(value.get('code') or value.get('value'))
					elif ctype == 'SPLIMAGE':
						if reference[0].get('value') == None:
							info[ctype].append('')
						else:
							splfile = reference[0].get('value').split()
							info[ctype].append(splfile)
					else:
						info[ctype].append(value.get('code') or value.get('value'))

			# If partCode is zero, we can find the <asContent> directly below the <manufacturedProduct> parent
			# else we need to iterate thorugh the <partProduct> of the <part>, from proceed() function



			if partCode == 'zero':
				level = parent
			else:
				level = partChild
			previous = []
			for child in level.xpath("./*[local-name() = 'subjectOf']"):
				try:
					for grandChild in child.xpath(".//*[local-name() = 'approval']"):
						statusCode = grandChild.xpath("./*[local-name() = 'code']")
						info['APPROVAL_CODE'].append(statusCode[0].get('code'))
				except:
					info['APPROVAL_CODE'].append('')
				#Get marketing act code
				for grandChild in child.xpath("./*[local-name() = 'marketingAct']"):
					statusCode = grandChild.xpath("./*[local-name() = 'statusCode']")

					info['MARKETING_ACT_CODE'].append(statusCode[0].get('code'))
				# Get policy code
				for grandChild in child.xpath("./*[local-name() = 'policy']"):
					for each in grandChild.xpath("./*[local-name() = 'code']"):
						info['DEA_SCHEDULE_CODE'].append(each.get('code'))
						info['DEA_SCHEDULE_NAME'].append(each.get('displayName'))

				for grandChild in child.xpath("./*[local-name() = 'characteristic']"):
					for each in grandChild.xpath("./*[local-name() = 'code']"):
						# Run each type through the CheckForValues() function above
						ctype = each.get('code')
						# checks for duplicate spl types, splcolor can happen twice
						if ctype in previous:
							idx = len(info[ctype]) - 1
							checkForValues(ctype, grandChild, '1', idx)
						else:
							idx = len(info[ctype])
							if idx < len(codes) - 1:
								info[ctype].append('')
							checkForValues(ctype, grandChild, '0', 0)
						previous.append(ctype)
						each.clear()   #clear memory
					grandChild.clear() #clear memory

		# Check if there are <parts> in the manufactured product, if not, partCode = 0
		parts = parent.xpath("./*[local-name() = 'part']")
		if not parts:
			# Check for child <manufacturedProduct>, if exists, check formCode
			childProduct = parent.xpath(".//*[local-name() = 'manufacturedProduct']")
			if childProduct:
				childFormCode = childProduct[0].xpath("./*[local-name() = 'formCode']")
				if childFormCode:
					if childFormCode[0].get('code') not in codeChecks:
						continue  #skip to next Manufactured Product
			# test current level FormCode against codeChecks
			formCode = parent.xpath("./*[local-name() = 'formCode']")
			if formCode:
				if formCode[0].get('code') not in codeChecks:
					continue
				else:
					formCodes.append(formCode[0].get('code'))
			# No parts found, so part number is zero, send to proceed() function
			proceed('zero','','')
		else:
			# Set up an index to pass to proceed() function to determine part number
			index = 1
			for child in parts:
				formCode =  child.xpath(".//*[local-name() = 'formCode']")

				# Check if formCode is in codeChecks
				if formCode[0].get('code') not in codeChecks:
					# If <part> <formCode> is not in codeChecks, move onto next <part>
					continue
				# else send to proceed() function with index
				else:
					getInfo()
					proceed(formCode[0].get('code'), child, index)
					index = index + 1
	prodMedicines.append(info)

	prodMedNames = [
					'SPLCOLOR','SPLIMAGE','SPLIMPRINT','medicine_name','SPLSHAPE',
					'SPL_INGREDIENTS','SPL_INACTIVE_ING','SPLSCORE','SPLSIZE',
					'product_code','part_num','dosage_code','MARKETING_ACT_CODE',
					'DEA_SCHEDULE_CODE','DEA_SCHEDULE_NAME','NDC','equal_product_code',
					'SPL_STRENGTH','part_medicine_name'
					]
	setInfoNames = ['file_name','effective_time','id_root','dailymed_date','setid','document_type','source']
	sponsorNames = ['author','author_type']

	# Loop through prodMedicines as many times as there are unique product codes + part codes combinations, which is len(codes)
	products = []

	if prodMedicines[0]['NDC']:
		for i in range(0, len(codes)):
			uniqueID = setInfo['setid'] + '-' + codes[i]
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

#Use this code to run xpath on the tmp-unzipped files without other scripts
if __name__ == "__main__":
	test = parseData("../tmp/tmp-unzipped/HRX/01F99FFF-4CD8-401F-9481-9CAC4E87BA2D.xml")
	print test
