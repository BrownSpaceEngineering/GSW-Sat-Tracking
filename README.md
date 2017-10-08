# GSW-Sat-Tracking

This is a project of Brown Space Engineering


Team members:
Trevor, Purvi, Kevin, Michael, Andrew.

## Goal

Provide backend calculations of important data for use in WebApp and mobile Apps.

# Documentation:

* userLocation

`userLocation() -> tuple(lon, lat)`

Returns a tuple representing user location.

* getTime

`getTime() -> {"time":<time>}`

Returns datetime element parsed into stringof current time.

* getSatLonLatAlt

`getSatLonLatAlt() -> {"loc":tuple(lon, lat, alt)}`

Returns a tuple representing satellite position.

* getSatLongitude

`getSatLongitude() -> {"lon":<lon>}`

Returns satellite longitude in degree.

* getSatLatitude

`getSatLatitude() -> {"lat":<lat>}`

Returns satellite latitude in degree.

* getSatAltitude

`getSatAltitude() -> {"alt":<alt>}`

Returns satellite altitude in km.

* getSatVelocityVector

`getSatVelocityVector() -> tuple(vx, vy, vz)`

Returns satellite velocity vector in km/s.

* getSatVelocity

`getSatVelocity() -> number(km/s)`

Returns satellite velocity in km/s.

* getAzEl

`getAzEl() -> {"az":<azimuth>,"el":<elevation>}`

Returns a tuple representing relative direction and elevation of satellite to user.

* getAzimuth

`getAzimuth() -> {"az": <azimuth>}`

Returns azimuth relative to the user in degree.

* getElevation

`getElevation() -> {"el":<elvation>}`

Returns elevation relative to the user in degree.

* getRADec

`getRADec() -> {"RA": <ra_value>, "DEC": <dec_value>}`

Returns elevation relative to the user as JSON string.

* getRA

`getRADec() -> number(deg)`

Returns right ascension of the satellite in degree.

* getDec

`getRADec() -> number(deg)`

Returns declination of the satellite in degree.  

* nextPass

'nextPass(location, body) -> {'rise_time':<rise_time>,'rise_azimuth': <rise_azimuth>,'max_alt_time':<max_alt_time>,"max_alt":<max_alt>,"set_time":<set_time>,"set_azimuth":<set_azimuth>}

* getVelocityVector

'getVelocityVector() -> {'velocity_vector': <velocity_vector>}'
