import copytext
import json
from flask import Flask, render_template, url_for

import settings

app = Flask(__name__, static_folder=settings.static_files_location, 
	        template_folder=settings.template_folders_location)

candidates = {}
copy = copytext.Copy(settings.copy_sheet_location)

for sheetName in copy.sheetNames():
	if sheetName == 'metadata':
		continue
	for row in copy[sheetName]:

		data = {}

		if row['Statement'].unescape() == "":
			data['statement'] = "The Daily Texan has no statement on file for this candidate"
		else:
			data['statement'] = row['Statement'].unescape()

		data['campaign_platform_points'] = []

		for point in row['Campaign Platform Points'].unescape().split('|||'):
			data['campaign_platform_points'].append(point)

		data['twitter_feed_url'] = row['Twitter Feed URL'].unescape()
		data['campaign_website'] = row['Campaign Website'].unescape()
		data['DT Coverage'] = []

		links = row['Daily Texan Coverage URLs'].unescape().split('|||')
		titles = row['Daily Texan Coverage Titles'].unescape().split('|||')

		for i in xrange(len(titles)):
			data['DT Coverage'].append({'title':titles[i], 'link':links[i]})

		candidateContext = {
			'headshot_photo_url': row['Photo URL'].unescape(),
			'headshot_photo_credit': row['Photo Credit'].unescape(),
			'candidate_name': row['Candidate Name'].unescape(),
			'major': row['Major'].unescape(),
			'year': row['Year'].unescape(),
			'json': json.dumps(data, ensure_ascii=False, separators=(',', ':'))
		}
		candidates[(row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_")] = candidateContext


@app.route('/candidates/<candidate_id>')
def candidate_page(candidate_id=None):
	context = candidates[candidate_id]
	return render_template('candidate.html', **context)

@app.route('/')
def navigation_page():
	context = {'navigation_json_link': url_for('static', 
		                                       filename='js/navigation.json')}
	return render_template('navigation.html', **context)

if __name__ == '__main__': app.run(debug = True)