import requests
import json

def getUserLoc():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	# print("latitude: " + str(lat))
	# print("longitude: " + str(lon))
	return (lat,lon)

def getISSLoc():
	send_url = "http://api.open-notify.org/iss-now.json"
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['iss_position']['latitude']
	lon = j['iss_position']['longitude']
	return (lat,lon)
