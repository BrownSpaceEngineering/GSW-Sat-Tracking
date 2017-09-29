# GSW-Sat-Tracking

This is a project of Brown Space Engineering


Team members:
Trevor, Purvi, Kevin, Michael, Andrew.

## Goal

Provide backend calculations of important data for use in WebApp and mobile Apps.

# Documentation:

###userLocation
`userLocation() -> tuple(lon, lat)`

Returns a tuple representing user location.

######getTime
`getTime() -> Datetime`

Returns datetime element of current time.

######getSatLonLatAlt
`getSatLonLatAlt() -> tuple(lon, lat, alt)`

Returns a tuple representing satellite position.

######getSatLongitude
`getSatLongitude() -> number(deg)`

Returns satellite longitude in degree.

######getSatLatitude
`getSatLatitude() -> number(deg)`

Returns satellite latitude in degree.

######getSatAltitude
`getSatAltitude() -> number(km)`

Returns satellite altitude in km.

######getSatVelocityVector
`getSatVelocityVector() -> tuple(vx, vy, vz)`

Returns satellite velocity vector in km/s.

######getSatVelocity
`getSatVelocity() -> number(km/s)`

Returns satellite velocity in km/s.

######getAzEl
`getAzEl() -> tuple(azimuth, elevation))`

Returns a tuple representing relative direction and elevation of satellite to user.

######getAzimuth
`getAzimuth() -> number(deg)`

Returns azimuth relative to the user in degree.

######getElevation
`getElevation() -> number(deg))`

Returns elevation relative to the user in degree.

######getRADec
`getRADec() -> tuple(right ascension, declination)`

Returns elevation relative to the user.

######getRA
`getRADec() -> number(deg)`

Returns right ascension of the satellite in degree.

######getDec
`getRADec() -> number(deg)`

Returns declination of the satellite in degree.  
