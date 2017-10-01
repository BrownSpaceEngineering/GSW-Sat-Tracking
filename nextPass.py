import ephem

LAT = "41:50"
##Latitude +North
LON = "-71:25"
##Longitude +East
ELEV = 50
##Elevation in meters
##DATE = 
##Date defaults to now()

location = ephem.Observer()
location.lon = LON
location.lat = LAT
location.elevation = ELEV

line1 = "ISS (ZARYA)"
line2 = "1 25544U 98067A   17274.41604447  .00005547  00000-0  91265-4 0  9999"
line3 = "2 25544  51.6420 228.7574 0004090 331.2642 175.1476 15.54036648 78276"
sat = ephem.readtle(line1, line2, line3)
print(sat)

def nextPass(location, body):
	return location.next_pass(body)
	##next_pass returns a six-element tuple giving:
	##0  Rise time
	##1  Rise azimuth
	##2  Maximum altitude time
	##3  Maximum altitude
	##4  Set time
	##5  Set azimuth

passData = nextPass(location, sat)
print(passData)