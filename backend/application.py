# import statements
import copytext
import json
from flask import Flask, render_template, url_for
import os
import sys
import urllib2

# give us the settings and methods to freeze this app
import settings

#init flask
app = Flask(__name__, static_folder=settings.static_files_location, 
	        template_folder=settings.template_folders_location)

#datawork
candidates = {}

copy = copytext.Copy('dataset.xlsx')

for sheetName in copy.sheetNames():
	if sheetName == 's1': 
		continue
	for row in copy[sheetName]:
		candidateContext = {
				'name' : row['cand_name'].unescape(),
				'occupation': row['occu'].unescape(),
				'biography': row['bio'].unescape(),
				'endorsements': row['endors'].unescape(),
				'platform': row['plat'].unescape(),
				'priority1': row['p1'].unescape(),
				'priority2': row['p2'].unescape(),
				'priority3': row['p3'].unescape(),
				'twitter': row['twit'].unescape(),
				'website': row['site'].unescape(),
				'photocred': row['pcred'].unescape(),
				'photo': row['purl'].unescape()
			}
	candidates = candidateContext
#routing
@app.route('/')
def main_page():
	context = candidates
	context['s1'] = copy['s1']
	return render_template('index.html', **context)
#debug
if __name__ == '__main__': app.run(debug = True)