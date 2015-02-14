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

		dtCoverage = []

		links = row['Daily Texan Coverage URLs'].unescape().split('|||')
		titles = row['Daily Texan Coverage Titles'].unescape().split('|||')

		for i in xrange(len(titles)):
			dtCoverage.append({'title':titles[i], 'link':links[i]})

		candidateId = (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_").replace("/", "_")
		candidatePhotoUrl = os.path.join('static', 'images', 'candidate_headshots', candidateId)

		candidateContext = {
			'headshot_photo_url': candidatePhotoUrl,
			'headshot_photo_credit': row['Photo Credit'].unescape(),
			'candidate_name': row['Candidate Name'].unescape(),
			'major': row['Major'].unescape(),
			'year': row['Year'].unescape(),
			'statement': "The Daily Texan has no statement on file for this candidate" if row['Statement'].unescape() == "" else row['Statement'].unescape(),
			'campaign_platform_points': row['Campaign Platform Points'].unescape().split('|||'),
			'twitter_feed_url': row['Twitter Feed URL'].unescape(),
			'campaign_website': row['Campaign Website'].unescape(),
			'dt_coverage': dtCoverage
		}
		candidates[candidateId] = candidateContext


@app.route('/candidates/<candidate_id>')
def candidate_page(candidate_id=None):
	context = candidates[candidate_id]
	return render_template('candidate.html', **context)

@app.route('/')
def navigation_page():
	context = {'navigation_json_link': url_for('static', 
		                                       filename='js/navigation.json').lstrip('/'),
				'global_css_link': url_for('static', 
					                           filename='css/global.css').lstrip('/'),
				'cover_image_link': url_for('static',
					                           filename='images/cover.jpg').lstrip('/')}
	return render_template('navigation.html', **context)

if __name__ == '__main__': app.run(debug = True)