from time import sleep
import pifacedigitalio as p
import sys
import http.client, urllib
import requests 
import json
import picamera

user_key = "ukMj9vug2AL8HH6NmK7hmJsSQAhHdq"
app_key = "azbKs62jHLN8UQocUeniEghNWxoncp"

imgur_client_id = "586603af3cd2743"
imgur_client_secret = "4e6b0ceaa2572ab98feb90051ecdb351800aa1ef"
imgur_pin="0aa7cedbb5"
imgur_auth_url = "https://api.imgur.com/oauth2/token"
imgur_auth_response = requests.post(imgur_auth_url,
	data={
		'client_id' : imgur_client_id,
		'client_secret' : imgur_client_secret,
		'grant_type': 'pin',
		'pin': imgur_pin,
	}
)
print(imgur_auth_response.text)
imgur_access_token = json.loads(imgur_auth_response.text)["access_token"]
print(imgur_acces_token)


import base64
from base64 import b64encode

headers = {"Authorization": "Bearer " + imgur_acces_token}
imgur_url = "https://api.imgur.com/3/upload.json"
		
res = requests.post(
	imgur_url,
	headers = headers,
	data ={
		'key': imgur_client_secret,
		'image': b64encode(open('foo.jpg', 'rb').read()),
		'type': 'base64',
		'name': 'foo.jpg',
		'title': 'someone at the door'
	}
)

print(res.text)




delay = 1
message = urllib.parse.urlencode({
				"token" : app_key,
				"user": user_key,
				"message": "button pushed",
			})

p.init()

p.digital_write(0,0)
p.digital_write(1,0)


while(True):
	if(p.digital_read(1) == 1):
		p.digital_write(0,1)
		conn = http.client.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json", message, 
			{"Content-type": "application/x-www-form-urlencoded"})
		conn.getresponse()
		p.digital_write(0,0)
		p.digital_write(1, 1)
		with picamera.PiCamera() as camera:
			camera.resolution = (1280, 720)
			camera.capture('foo.jpg')			
		p.digital_write(1,0)
	
	p.digital_write(1,1)
	p.digital_write(1,0)
	sleep(delay)
	