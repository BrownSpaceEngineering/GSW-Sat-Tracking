import requests
from pyorbital.orbital import Orbital
from datetime import datetime
import calendar
import json
import urllib
import threading
import atexit
import time
import ephem
import re

DEFAULT_TLE_FILE = "tle.txt"
EQUISAT_TLE_FILE = "equisat-tle.txt"
TLE_UPDATE_PERIOD_S = 3*60*60
UPDATE_SOURCES = [
    "https://www.celestrak.com/NORAD/elements/stations.txt",
    # "https://www.celestrak.com/NORAD/elements/tle-new.txt",
    "https://www.celestrak.com/NORAD/elements/cubesat.txt"
]

def convert_ephem_float_to_date(float_date):
    return ephem.Date(float_date)

def convert_unix_time_to_date(float_date):
    return datetime.fromtimestamp(float_date)

def update_TLE():
    print("%s: updating TLEs" % datetime.now())
    with open(DEFAULT_TLE_FILE, 'w') as tle_file:
        for url in UPDATE_SOURCES:
            r = urllib.request.urlopen(url)
            tle_file.write(r.read().decode('utf-8'))
    extractEQUiSatTLE()

def get_ip_loc():
    url = 'http://ipinfo.io/json'
    r = requests.get(url)
    if(r.status_code != requests.codes.ok):
        return None, False
    j = json.loads(r.text)
    location = j['loc']
    # We receive the location as a "lat,lon" string, with values separated by a comma
    lat = location.split(',')[0]
    lon = location.split(',')[1]
    return (lon,lat,0), True

def get_ISS_loc():
    url = "http://api.open-notify.org/iss-now.json"
    r = requests.get(url)
    j = json.loads(r.text)
    lat = j['iss_position']['latitude']
    lon = j['iss_position']['longitude']
    return (lat,lon)

def get_orbital(sat, file_path=DEFAULT_TLE_FILE):
    orb = Orbital(sat, file_path)
    return orb

def get_TLE(sat, file_path=DEFAULT_TLE_FILE):
    tle_file = open(file_path, 'r')
    s = tle_file.read()
    tle_list = [x.split(" ") for x in s.split("\n")]
    for i in range(0, len(tle_list)):
        if " ".join(tle_list[i]).strip() == sat:
            tle = [" ".join(tle_list[i]).strip(), " ".join(tle_list[i+1]), " ".join(tle_list[i+2])]
            return tle

def ephem_to_unix(ephemdate):
    """ Converts pyephem date into POSIX unix time float (secs.ms since 1/1/1970) """
    return calendar.timegm(ephemdate.datetime().utctimetuple())

# tle update helpers
def start_update_tle_daemon():
    tle_update_thread = threading.Thread(target=update_tle_cb)
    tle_update_thread.setDaemon(True)
    tle_update_thread.start()

def update_tle_cb():
    while True:
        time.sleep(TLE_UPDATE_PERIOD_S) # we don't care too much about clock drift
        update_TLE()

def extractEQUiSatTLE():
    with open(DEFAULT_TLE_FILE, 'r') as tle_file:
        tles_str = tle_file.read()
        equisat_tle = re.search("EQUISAT(.*\n){3}", tles_str)
        if (equisat_tle == None):
            equisat_tle = re.search("ISS \(ZARYA\)(.*\n){3}", tles_str)
        if (equisat_tle):
            with open(EQUISAT_TLE_FILE, "w+") as equisat_tle_file:
                equisat_tle_file.write(equisat_tle.group()[:-1])

if __name__ == '__main__':
    print("updating tle")
    update_TLE()
