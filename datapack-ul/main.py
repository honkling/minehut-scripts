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
		print('What is the name of the world?')
		wname = input()
		
		clear()
		print('What is the name of the datapack? (any name)')
		dname = input()
		path = "/" + wname + "/datapacks/" + dname

		clear()
		print('Where is the datapack? (directory path)')
		upload = input()

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
		recursive(auth, id, upload, path)

	except KeyError:
		clear()
		print('Couldn\'t find server!')
		printname()

def recursive(auth, id, upload, path):
	print('Creating folder {0}'.format(path))
	split = path.split('/')
	requests.post('{0}/file/{1}/folder/create'.format(BASE_URL, id), headers=auth, json={"directory":'/'.join(split[:(len(split)-1)]),"name":split[-1]})
	print('Getting all files in path {0}'.format(upload))
	for i in os.listdir(upload):
		joined = os.path.join(upload, i)
		if os.path.isfile(joined):
			print('Uploading file {0}'.format(joined))
			r = requests.post('{0}/file/upload/{1}/{2}/{3}'.format(BASE_URL, id, path, i), headers=auth, files={"file":open(joined,'rb')})
			if r.status_code == 200:
				print('Successfully uploaded {0} to {1}/{2}'.format(joined, path, i))
			else:
				print('Failed to upload {0} to {1}/{2}: {3} {4}'.format(joined, path, i, r.status_code, r.json()))
		else:
			recursive(auth, id, joined, '{0}/{1}'.format(path, i))

import requests, json, os

BASE_URL = 'https://api.minehut.com'

clear()

printname()
