import os
import urllib2

import copytext

def download_images(static_files_location, copy_sheet_location):
	destination = os.path.join(static_files_location, 'images', 'candidate_headshots')
	copy = copytext.Copy(copy_sheet_location)
	sheetNames = copy.sheetNames()

	for name in sheetNames:
		if name == 'metadata':
			continue
		for row in copy[name]:
			candidateId = (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_").replace("/", "_")
			destinationForPhoto = os.path.join(destination, candidateId)
			if row['Photo URL'] != "":
				download(row['Photo URL'].unescape(), destinationForPhoto)
			else:
				with open(destinationForPhoto + '.jpg', 'wb') as f:
					with open('default.jpg', 'rb') as g:
						f.write(g.read())

			destinationForPhoto += "_thumbnail"
			if row['Thumbnail URL'] != "":
				download(row['Thumbnail URL'].unescape(), destinationForPhoto)
			else:
				with open(destinationForPhoto + '.jpg', 'wb') as f:
					with open('default_thumbnail.jpg', 'rb') as g:
						f.write(g.read())

def download(url, destination):
	page = urllib2.urlopen(url)
	content = page.read()
	page.close()
	with open(destination + '.' + url.split('.')[-1], 'wb') as f:
		f.write(content)