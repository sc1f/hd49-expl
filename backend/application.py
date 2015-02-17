import copytext
import json
from flask import Flask, render_template, url_for
import os
import sys
import urllib2
from bs4 import BeautifulSoup

import settings
from make_navigation import make_navigation
from localize_assets import download_images

app = Flask(__name__, static_folder=settings.static_files_location, 
	        template_folder=settings.template_folders_location)

candidates = {}
copy = copytext.Copy(settings.copy_sheet_location)

for sheetName in copy.sheetNames():
	if sheetName == 'metadata':
		continue
	for row in copy[sheetName]:

		dtCoverage = []

		links = row['Daily Texan Coverage URLs'].unescape().split('|||') if len(row['Daily Texan Coverage URLs'].unescape()) != 0 else []
		titles = row['Daily Texan Coverage Titles'].unescape().split('|||') if len(row['Daily Texan Coverage Titles'].unescape()) != 0 else []

		for i in xrange(len(titles)):
			dtCoverage.append({'title':titles[i], 'link':links[i]})

		try:
			campaign_website_title = BeautifulSoup(urllib2.urlopen(row['Campaign Website'].unescape())).title.string if len(row['Campaign Website'].unescape()) != 0 else ""
		except:
			print str(row['Campaign Website'].unescape()) + ": ERROR! - " + str(sys.exc_info()[0])
			campaign_website_title = row['Candidate Name'].unescape() + " Campaign Website"

		candidateContext = {
			'headshot_photo_credit': row['Photo Credit'].unescape(),
			'candidate_name': row['Candidate Name'].unescape(),
			'major': row['Major'].unescape(),
			'year': row['Year'].unescape(),
			'statement': "The Daily Texan has no statement on file for this candidate" if row['Statement'].unescape() == "" else row['Statement'].unescape(),
			'campaign_platform_points': row['Campaign Platform Points'].unescape().split('|||') if len(row['Campaign Platform Points'].unescape()) != 0 else [],
			'twitter_feed_url': row['Twitter Feed URL'].unescape(),
			'twitter_user_name': row['Twitter Feed URL'].unescape().split('/')[-1],
			'campaign_website': row['Campaign Website'].unescape(),
			'campaign_website_title': campaign_website_title,
			'dt_coverage': dtCoverage
		}
		candidateId = (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_").replace("/", "_")

		candidates[candidateId] = candidateContext

make_navigation(settings.copy_sheet_location, settings.web_app_location, 
		            settings.static_files_location)
download_images(settings.static_files_location, settings.copy_sheet_location)

@app.route('/candidates/<candidate_id>')
def candidate_page(candidate_id=None):
	context = candidates[candidate_id]
	candidateId = (context['candidate_name'] + context['major'] + context['year']).replace(" ", "_").replace("/", "_")
	candidatePhotoUrl = url_for('static', 
			                     filename='images/candidate_headshots/' + candidateId + '.jpg')
	context['headshot_photo_url'] = candidatePhotoUrl
	context['candidate_styling'] = url_for('static', filename='css/candidate.css')
	context['cover_image_link'] = url_for('static',
					                      filename='images/cover_candidate.jpg')

	return render_template('candidate.html', **context)

@app.route('/')
def navigation_page():
	context = {'navigation_json_link': url_for('static', 
		                                       filename='js/navigation.json'),
				'global_css_link': url_for('static', 
					                           filename='css/global.css'),
				'cover_image_link': url_for('static',
					                           filename='images/cover.jpg')}
	return render_template('navigation.html', **context)

if __name__ == '__main__': app.run(debug = True)