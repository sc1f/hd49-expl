from flask_frozen import Freezer
import copytext
from application import app

import settings

def generate():
	app.config['FREEZER_DESTINATION'] = settings.web_app_location
	app.config['FREEZER_BASE_URL'] = settings.external_url

	freezer = Freezer(app)

	copy = copytext.Copy('dataset.xlsx')
	@freezer.register_generator
	def main_page():
		for sheetName in copy.sheetNames():
			if sheetName == 's1' : continue
				
	freezer.freeze()

if __name__ == '__main__': generate()