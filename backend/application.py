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

#datawork
copy = copytext.Copy('dataset.xlsx')

for row in copy['s1']:
	candidateContext = {
			'name': row['cand_name'].unescape()
			'occupation': row['occu'].unescape()
			'biography': row['bio'].unescape()

		}

#routing
@app.route('/')
def main_page():
	context = {
        'COPY': copytext.Copy('dataset.xlsx')
    }
	return render_template('index.html', **context)
#debug
if __name__ == '__main__': app.run(debug = True)