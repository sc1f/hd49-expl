# import statements
import copytext
import json
from flask import Flask, render_template, url_for
import os
import sys
import urllib2
from bs4 import BeautifulSoup

# give us the settings and methods to freeze this app
import settings

#init flask
app = Flask(__name__, static_folder=settings.static_files_location, 
	        template_folder=settings.template_folders_location)

candidates = {}
#run copytext
copy = copytext.Copy(settings.copy_sheet_location)
#for each sheet of candidates, start generating data
for sheetName in copy.sheetNames(): 

	for row in copy[sheetName]:

		try:
			#checks if sites are accessible
			campaign_website_title = BeautifulSoup(urllib2.urlopen(row['Campaign Website'].unescape())).title.string if len(row['Campaign Website'].unescape()) != 0 else ""
		except:
			#if not accesssible throw error
			print str(row['Campaign Website'].unescape()) + ": ERROR! - " + str(sys.exc_info()[0])
			campaign_website_title = row['Candidate Name'].unescape() + " Campaign Website"
		#parses the copy
		candidateContext = {
			'headshot_photo_credit': "Credit: " + row['Photo Credit'].unescape() if row['Photo Credit'].unescape() != "" else "Photo courtesy of the candidate",
			'candidate_name': row['Candidate Name'].unescape(),
			'occupation': row['Occupation'].unescape(),
			'biography': row['Biography'].unescape(),
			'endorsements': row['Endorsements'].unescape(),
			'campaign_platform_points': row['Platform'].unescape(),
			'priority1': row['Priority 1'].unescape(),
			'priority2': row['Priority 2'].unescape(),
			'priority3': row['Priority 3'].unescape(),
			'twitter_feed_url': row['Twitter'].unescape(),
			'twitter_user_name': row['Twitter'].unescape().split('/')[-1],
			'campaign_website': row['Campaign Website'].unescape(),
			'campaign_website_title': campaign_website_title
		}
		#generate a custom ID for each candidate
		candidateId = row['Candidate Name'].unescape().replace(" ", "_").replace("/", "_")
		#imports context data into candidates var?
		candidates[candidateId] = candidateContext
#routing
@app.route('/<candidate_id>.html')
def candidate_page(candidate_id=None):
	context = candidates[candidate_id]
	candidateId = context['Candidate Name'].unescape().replace(" ", "_").replace("/", "_")
	candidatePhotoUrl = url_for('static', 
			                     filename='images/headshots/' + candidateId + '.jpg')
	context['headshot_photo_url'] = candidatePhotoUrl
	context['candidate_styling'] = url_for('static', filename='css/candidate.css')
	context['cover_image_link'] = url_for('static',
					                     	filename='images/cover_candidate.jpg')

	return render_template('candidate.html', **context)

@app.route('/')
def navigation_page():
	context = {'js_link': url_for('static', 
		                                       filename='js/main.js'),
				'global_css_link': url_for('static', 
					                           filename='css/styles.css')}
	return render_template('index.html', **context)

# @app.route('/attribution.html')
# def attribution_page():
# 	context = {}

if __name__ == '__main__': app.run(debug = True)