from flask_frozen import Freezer
import copytext
from application import app

import settings

def generate():
	app.config['FREEZER_DESTINATION'] = settings.web_app_location
	app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
	app.config['FREEZER_RELATIVE_URLS'] = True

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