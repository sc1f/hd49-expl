from flask_frozen import Freezer
import copytext
from application import app

import settings

def generate():
	app.config['FREEZER_DESTINATION'] = settings.web_app_location
	app.config['FREEZER_BASE_URL'] = settings.external_url

	freezer = Freezer(app)

	copy = copytext.Copy(settings.copy_sheet_location)
	@freezer.register_generator
	def candidate_page():
		for sheetName in copy.sheetNames():
			if sheetName == 'metadata' or sheetName == 'Attribution': continue
			for row in copy[sheetName]:
				yield {"candidate_id": row['Candidate Name'].unescape().replace(" ", "_").replace("/", "_")}
				
	freezer.freeze()

if __name__ == '__main__': generate()