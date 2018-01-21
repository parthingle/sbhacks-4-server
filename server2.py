import socket
import asyncio
import json 
import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from geopy.distance import vincenty

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sbhacks4-9f27c.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('restricted_access/secret_document/users') ### What does this argument mean?
match_branch = db.reference('restricted_access/secret_document/match')
count = 0
change_flag = 0
try:
	while(1):
		poll = ref.get()
		poll_keys = list(poll.keys())
		for key in range (len(poll_keys)):
			for j in range (1, len(list(poll.keys()))):
				if(poll[poll_keys[key]]['artist'] == poll[poll_keys[j]]['artist']):
					entry1 = (poll[poll_keys[key]]['lat'], poll[poll_keys[key]]['long'])
					entry2 = (poll[poll_keys[j]]['lat'], poll[poll_keys[j]]['long'])
					if(vincenty(entry1, entry2).meters < 200):
						message_json = {'client1' : poll[poll_keys[key]]['user-id'],  'client2' : poll[poll_keys[j]]['user-id']}
						entry = match_branch.push(message_json)
		time.sleep(1)
		print('lol')

except KeyboardInterrupt:
	print("Closing Server")
	pass