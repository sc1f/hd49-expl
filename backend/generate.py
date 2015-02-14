from flask_frozen import Freezer
import copytext
from application import app

import settings
from make_navigation import make_navigation
from localize_assets import download_images

def generate():
	make_navigation(settings.copy_sheet_location, settings.web_app_location, 
		            settings.static_files_location)
	download_images(settings.static_files_location, settings.copy_sheet_location)

	app.config['FREEZER_DESTINATION'] = settings.web_app_location
	app.debug = True
	app.testing = True
	freezer = Freezer(app)

	copy = copytext.Copy(settings.copy_sheet_location)
	@freezer.register_generator
	def candidate_page():
		for sheetName in copy.sheetNames():
			if sheetName == 'metadata': continue
			for row in copy[sheetName]:
				yield {"candidate_id": (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_").replace("/", "_")}
				# yield '/candidates/' + (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_")
	
	freezer.freeze()

if __name__ == '__main__': generate()