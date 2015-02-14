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
			if row['Photo URL'] != "":
				candidateId = (row['Candidate Name'].unescape() + row['Major'].unescape() + row['Year'].unescape()).replace(" ", "_").replace("/", "_")
				destinationForPhoto = os.path.join(destination, candidateId)
				download(row['Photo URL'].unescape(), destinationForPhoto)

def download(url, destination):
	page = urllib2.urlopen(url)
	content = page.read()
	page.close()
	with open(destination + '.' + url.split('.')[-1], 'wb') as f:
		f.write(content)