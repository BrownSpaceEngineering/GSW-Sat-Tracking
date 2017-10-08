import requests
from pyorbital.orbital import Orbital
import json
import urllib

def update_TLE():
	url = "https://www.celestrak.com/NORAD/elements/stations.txt"
	r = urllib.request.urlopen(url)
	tle_file = open("tle.txt", "w")
	tle_file.write(r.read().decode('utf-8'))
	tle_file.close()

def get_user_loc():
	url = 'http://freegeoip.net/json'
	r = requests.get(url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	# print("latitude: " + str(lat))
	# print("longitude: " + str(lon))
	return (lat,lon)

def get_ISS_loc():
	url = "http://api.open-notify.org/iss-now.json"
	r = requests.get(url)
	j = json.loads(r.text)
	lat = j['iss_position']['latitude']
	lon = j['iss_position']['longitude']
	return (lat,lon)

def get_orbital(sat):
	file_path = "tle.txt"
	orb = Orbital(sat, file_path)
	return orb

def get_TLE(sat):
	file_path = "tle.txt"
	tle_file = open(file_path, 'r')
	s = tle_file.read()
	tle_list = [x.split(" ") for x in s.split("\n")]
	for i in range(0, len(tle_list)):
		if tle_list[i][0] is sat:
			tle = [" ".join(tle_list[i]), " ".join(tle_list[i+1]), " ".join(tle_list[i+2])]
			return tle
