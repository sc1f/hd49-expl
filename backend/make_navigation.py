import json
import os

import copytext

def make_navigation(copy_sheet_location, web_app_location, static_files_location):
	copy = copytext.Copy(copy_sheet_location)
	sheetNames = copy.sheetNames()
	data = {}
	for name in sheetNames:
		if name == 'metadata' or name =='Attribution':
			continue
		initials = name[name.find('(')+1:name.find(')')]
		objectToAdd = {}
		objectToAdd['full_name'] = name[0:name.find('(') - 1]
		objectToAdd['purpose_paragraph'] = copy['metadata'][name]['purpose'].unescape()
		objectToAdd['categories'] = {}
		for row in copy[name]:
			objectToAdd['categories'][row['Category'].unescape()] = {"subcategories":{},
			                                                         "visibility_of_subcategories":"hidden"}

		for row in copy[name]:
			subcategories = objectToAdd['categories'][row['Category'].unescape()]['subcategories']
			if (row['Subcategory'].unescape() != ""):
				objectToAdd['categories'][row['Category'].unescape()]['visibility_of_subcategories'] = "visible"
			subcategories[row['Subcategory'].unescape()] = {'candidates':[],
			                                                'numPositions': int(float(row['Category Number'].unescape()))}

		for row in copy[name]:
			subcategories = objectToAdd['categories'][row['Category'].unescape()]['subcategories']
			arrayToAddTo = subcategories[row['Subcategory'].unescape()]['candidates']
			candidate = {}
			candidate['Name'] = row['Candidate Name'].unescape()
			candidateId = (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_").replace("/", "_")
			candidate['photo_url'] = os.path.join('static', 'images', 'candidate_headshots', candidateId) + '_thumbnail.jpg'
			candidate['position'] = row['Position'].unescape()
			candidate['detail_page_url'] = 'candidates/' + candidateId + '.html'
			arrayToAddTo.append(candidate)

		data[initials] = objectToAdd

	with open(os.path.join(static_files_location, 'js', 'navigation.json'),
		      mode='w') as f:
		json.dump(data, f, ensure_ascii=True,separators=(',', ':'))