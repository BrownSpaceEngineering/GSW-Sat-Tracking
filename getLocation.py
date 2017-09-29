import requests
import json

def getLoc():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	# print("latitude: " + str(lat))
	# print("longitude: " + str(lon))
	return (lat,lon)
