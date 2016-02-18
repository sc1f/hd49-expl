from flask_frozen import Freezer
import copytext
from application import app

import settings

freezer = Freezer(app)

if __name__ == '__main__': 
	freezer.freeze()