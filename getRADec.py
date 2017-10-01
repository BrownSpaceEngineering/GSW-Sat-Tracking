import ephem

# Gets the DEC (Declination) and RA (Right acension)
# for the epoch specified
def getRADec(epoch):
    return (epoch.ra, epoch.dec)
