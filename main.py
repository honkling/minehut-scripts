def clear():
	print('\n' * 250)

def printname():
	print('What is the name of your server? (ID will be grabbed automatically)')
	name = input()
	r = requests.get('{0}/server/{1}?byName=true'.format(BASE_URL, name)).json()
	try:
		r["server"]["_id"]
		id = r["server"]["_id"]
		
		clear()
		print('What file do you want to download? (Directories allowed, path MUST start with \'/\')')
		path = input()
		folder = not '.' in path[(len(path)-7):]

		clear()
		print('Where do you want to download the file to? (directory path)')
		download = input()
		if not os.path.exists(download):
			os.mkdir(download)

		clear()
		print('What\'s your authorization token? (View https://app.gitbook.com/@honkling/s/minehut-api for info on how to retrieve authentication values)')
		token = input()

		clear()
		print('What\'s your session id? (View https://app.gitbook.com/@honkling/s/minehut-api for info on how to retrieve authentication values)')
		session = input()

		auth = {
			"authorization": token,
			"x-session-id": session
		}

		clear()
		recursive(auth, id, download, path, folder)

	except KeyError:
		clear()
		print('Couldn\'t find server!')
		printname()

def recursive(auth, id, download, path, folder):
	print('Getting files at path {0}'.format(path))
	r = requests.get('{0}/file/{1}/{2}/{3}'.format(BASE_URL, id, "list" if folder else "read", path), headers=auth).json()
	if folder:
		try:
			r["files"]
			for i in r["files"]:
				if not i["blocked"]:
					print('Found file/directory! {0}'.format(i["name"]))
					if not i["directory"]:
						print('Writing file {0} to path {1}/{2}'.format(i["name"], download, i["name"]))
						with open('{0}/{1}'.format(download, i["name"]), 'w') as f:
							content = requests.get('{0}/file/{1}/read/{2}'.format(BASE_URL, id, '{0}/{1}'.format(path, i["name"])), headers=auth).json()
							f.write(content["content"])
					else:
						if not os.path.exists('{0}/{1}'.format(download, i["name"])):
							os.mkdir('{0}/{1}'.format(download, i["name"]))
						recursive(auth, id, '{0}/{1}'.format(download, i["name"]), '{0}/{1}'.format(path, i["name"]), folder)
		except KeyError:
			print('Couldn\'t get the file list at {0}! Response: {1}'.format(path, r))
	else:
		content = requests.get('{0}/file/{1}/read/{2}'.format(BASE_URL, id, path))
		with open('{0}/{1}'.format(download, path), 'w') as f:
			f.write(content["content"])

import requests, json, os

BASE_URL = 'https://api.minehut.com'

clear()

printname()
