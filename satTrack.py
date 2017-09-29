from pyorbital import tlefile
from datetime import datetime
from pyorbital.orbital import Orbital
from getLocation import getLoc

satellite = "ISS"
filepath = "stations.txt"
orb = Orbital(satellite, filepath)
now = datetime.utcnow()
myLat = getLoc()[0]
myLon = getLoc()[1]
myAlt = 0

# normPos = orb.get_position(now, normalize=False)
# print("Normalized position and velocity of satellite: " + str(normPos))
# print("My Latitude: " + str(myLat))
# print("My Longitude: " + str(myLon))

#returns velocity of satellite in array (x y z)
def getVelocity():
	normPos = orb.get_position(now, normalize=False)
	vel = normPos[1]
	print("Velocity vector: " + str(vel))
	return vel

#returns angle of satellite relative to your position as tuple: (azimuth, elevation)
def getAngle():
	angle = orb.get_observer_look(now,myLon, myLat,myAlt)
	print("Angle of elevation: " + str(angle))
	return angle

#returns satellite's lon, lat, and alt as tuple: (longitude, latitude, altitude)
def getSatLonLatAlt():
	lonlatalt = orb.get_lonlatalt(now)
	print("Lon, lat, alt: " + str(lonlatalt))
	return lonlatalt

# def getNextPasses():
# 	nextPasses = orb.get_next_passes(now, 2, myLon, myLat, myAlt, tol=0.0001, horizon=0)
# 	print ("Next passes: " + str(nextPasses))
# 	return nextPasses

getVelocity()
getAngle()
getSatLonLatAlt()
# getNextPasses()