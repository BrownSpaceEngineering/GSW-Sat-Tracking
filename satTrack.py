from pyorbital import tlefile
from datetime import datetime
from pyorbital.orbital import Orbital
from getLocation import getUserLoc
from getLocation import getISSLoc
from math import sqrt
import json
satellite = "ISS"
filepath = "stations.txt"
orb = Orbital(satellite, filepath)

def userLocation(user):
	return getUserLoc()

# normPos = orb.get_position(now, normalize=False)
# print("Normalized position and velocity of satellite: " + str(normPos))
# print("My Latitude: " + str(myLat))
# print("My Longitude: " + str(myLon))

#returns velocity of satellite in array (x y z)
def getVelocityVector():
	normPos = orb.get_position(now, normalize=False)
	vel = normPos[1]
	print("Velocity vector: " + str(vel))
	d = {
		'velocity_vector': vel
	}
	return json.dumps(d)

def getVelocity():
	now = datetime.utcnow()
	normPos = orb.get_position(now, normalize=False)
	vel = normPos[1]
	v = sqrt(sum(map(lambda x: x**2, vel)))
	return v

#returns angle of satellite relative to your position as tuple: (azimuth, elevation)
def getAzEl():
	myLat = userLocation("")[0]
	myLon = userLocation("")[1]
	myAlt = 0
	azEl = orb.get_observer_look(datetime.utcnow(),myLon, myLat,myAlt)
	d = {
		'az' : azEl[0],
		'el': azEl[1]
	}
	return json.dumps(d)

#returns azimuth and elevation separately
def getAzimuth():
	myLat = userLocation("")[0]
	myLon = userLocation("")[1]
	myAlt = 0
	azEl = orb.get_observer_look(datetime.utcnow(),myLon, myLat,myAlt)
	d = {
		'az' : azEl[0]
	}
	return json.dumps(d)

def getElevation():
	myLat = userLocation("")[0]
	myLon = userLocation("")[1]
	myAlt = 0
	azEl = orb.get_observer_look(datetime.utcnow(),myLon, myLat,myAlt)
	d = {
		'el' : azEl[1]
	}
	return json.dumps(d)

#returns satellite's lon, lat, and alt as tuple: (longitude, latitude, altitude)
def getSatLonLatAlt():
	lonlatalt = orb.get_lonlatalt(datetime.utcnow())
	d = {
		'loc' : lonlatalt
	}
	return json.dumps(d)

#returns sattellite's individual lon, lat and alt
def getSatLongitude():
	lonlatalt = orb.get_lonlatalt(datetime.utcnow())
	d = {
		'lon' : lonlatalt[0]
	}
	return json.dumps(d)

def getSatLatitude():
	lonlatalt = orb.get_lonlatalt(datetime.utcnow())
	d = {
		'lat' : lonlatalt[1]
	}
	return json.dumps(d)

def getSatAltitude():
	lonlatalt = orb.get_lonlatalt(datetime.utcnow())
	d = {
		'alt' : lonlatalt[2]
	}
	return json.dumps(d)

def getTime():
	time = datetime.utcnow()
	d = {
		'time' : time.strftime('%Y-%m-%dT%H:%M:%S')
	}
	return json.dumps(d)

# def getNextPasses():
# 	nextPasses = orb.get_next_passes(now, 2, myLon, myLat, myAlt, tol=0.0001, horizon=0)
# 	print ("Next passes: " + str(nextPasses))
# 	return nextPasses

getVelocity()
getAzEl()
getSatLonLatAlt()
getTime()
# getNextPasses()
