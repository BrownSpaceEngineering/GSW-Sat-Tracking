from pyorbital import tlefile
from datetime import datetime
from pyorbital.orbital import Orbital
from getLocation import getLoc

#read in TLE file
# tle = tlefile.read('ISS', "/home/kevin/Documents/BSE/stations.txt")
# print("Inclination: " + str(tle.inclination))

#read in TLE for ISS
satellite = "ISS"
filepath = "stations.txt"
orb = Orbital(satellite, filepath)
now = datetime.utcnow()
normPos = orb.get_position(now)
print("Normalized position and velocity of satellite: " + str(normPos))
lonlatalt = orb.get_lonlatalt(now)
print("Lon, lat, alt: " + str(lonlatalt))
myLat = getLoc()[0]
print("My Latitude: " + str(myLat))
myLon = getLoc()[1]
print("My Longitude: " + str(myLon))

angle = orb.get_observer_look(now,myLon, myLat,0)
print("Angle of elevation: " + str(angle))