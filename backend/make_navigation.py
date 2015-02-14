import json
import os

import copytext

def make_navigation(copy_sheet_location, web_app_location, static_files_location):
	copy = copytext.Copy(copy_sheet_location)
	sheetNames = copy.sheetNames()
	data = {}
	for name in sheetNames:
		if name == 'metadata':
			continue
		initials = name[name.find('(')+1:name.find(')')]
		objectToAdd = {}
		objectToAdd['full_name'] = name[0:name.find('(') - 1]
		objectToAdd['purpose_paragraph'] = copy['metadata'][name]['purpose'].unescape()
		objectToAdd['categories'] = {}
		for row in copy[name]:
			objectToAdd['categories'][row['Category'].unescape()] = {"candidates": {"subcategories":{},
			                                                                        "visibility_of_subcategories":"hidden"}}

		
		for row in copy[name]:
			candidates = objectToAdd['categories'][row['Category'].unescape()]['candidates']
			if (row['Subcategory'].unescape() != ""):
				candidates['visibility_of_subcategories'] = "visible"
			candidates['subcategories'][row['Subcategory'].unescape()] = []

		for row in copy[name]:
			candidates = objectToAdd['categories'][row['Category'].unescape()]['candidates']
			arrayToAddTo = candidates['subcategories'][row['Subcategory'].unescape()]
			candidate = {}
			candidate['Name'] = row['Candidate Name'].unescape()
			candidate['photo_url'] = row['Photo URL'].unescape()
			candidate['position'] = row['Position'].unescape()
			candidate['detail_page_url'] = 'candidates/' + row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()
			candidate['detail_page_url'].replace(" ", "_").replace('/', '_')
			arrayToAddTo.append(candidate)

		data[initials] = objectToAdd

	with open(os.path.join(static_files_location, 'js', 'navigation.json'),
		      mode='w') as f:
		json.dump(data, f, ensure_ascii=True,separators=(',', ':'))