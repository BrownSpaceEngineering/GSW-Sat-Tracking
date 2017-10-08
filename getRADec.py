import ephem
import json
# Gets the DEC (Declination) and RA (Right acension)
# for the epoch specified
def getRADec(epoch):
	ra = epoch.ra
	dec = epoch.dec 
	d = {
		'RA' : ra,
		'DEC' : dec
	}
    return (json.dumps(d))
