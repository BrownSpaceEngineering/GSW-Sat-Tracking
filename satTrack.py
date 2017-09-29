from pyorbital import tlefile
from datetime import datetime
from pyorbital.orbital import Orbital
from getLocation import getLoc
from math import sqrt

satellite = "ISS"
filepath = "stations.txt"
orb = Orbital(satellite, filepath)

def userLocation(user):
	return getLoc()

# normPos = orb.get_position(now, normalize=False)
# print("Normalized position and velocity of satellite: " + str(normPos))
# print("My Latitude: " + str(myLat))
# print("My Longitude: " + str(myLon))

#returns velocity of satellite in array (x y z)
def getVelocityVector():
	normPos = orb.get_position(now, normalize=False)
	vel = normPos[1]
	print("Velocity vector: " + str(vel))
	return vel

def getVelocity():
	v = sqrt(sum(map(lambda x: x**2, getVelocityVector())))
	return v

#returns angle of satellite relative to your position as tuple: (azimuth, elevation)
def getAzEl():
	myLat = userLocation("")[0]
	myLon = userLocation("")[1]
	myAlt = 0
	azEl = orb.get_observer_look(getTime(),myLon, myLat,myAlt)
	return azEl

#returns azimuth and elevation separately
def getAzimuth():
	return getAzEl()[0]

def getElevation():
	return getAzEl()[1]

#returns satellite's lon, lat, and alt as tuple: (longitude, latitude, altitude)
def getSatLonLatAlt():
	lonlatalt = orb.get_lonlatalt(getTime())
	return lonlatalt

#returns sattellite's individual lon, lat and alt
def getSatLongitude():
	return getSatLonLatAlt()[0]

def getSatLatitude():
	return getSatLonLatAlt()[1]

def getSatAltitude():
	return getSatLonLatAlt()[2]

def getTime():
	time = datetime.utcnow()
	return time

# def getNextPasses():
# 	nextPasses = orb.get_next_passes(now, 2, myLon, myLat, myAlt, tol=0.0001, horizon=0)
# 	print ("Next passes: " + str(nextPasses))
# 	return nextPasses

getVelocity()
getAzEl()
getSatLonLatAlt()
getTime()
# getNextPasses()
