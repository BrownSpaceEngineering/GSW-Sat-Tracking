import requests
from pyorbital.orbital import Orbital
from datetime import datetime
import json
import urllib
import threading, atexit
import ephem

DEFAULT_TLE_FILE = "equisat-tle.txt"
TLE_UPDATE_PERIOD_S = 3*60*60

def convert_ephem_float_to_date(float_date):
    return ephem.Date(float_date)

def update_TLE():
    with open(DEFAULT_TLE_FILE, 'w') as tle_file:
        # Make file blank
        tle_file.truncate(0)
        # Space Stations
        url = "https://www.celestrak.com/NORAD/elements/stations.txt"
        r = urllib.request.urlopen(url)
        tle_file.write(r.read().decode('utf-8'))
        # Cubesats
        url = "https://www.celestrak.com/NORAD/elements/cubesat.txt"
        r = urllib.request.urlopen(url)
        tle_file.write(r.read().decode('utf-8'))

def get_ip_loc():
    url = 'http://freegeoip.net/json'
    r = requests.get(url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    # print("latitude: " + str(lat))
    # print("longitude: " + str(lon))
    return (lon,lat,0)

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

def time(self):
    return datetime.utcnow()

def ephem_to_unix(ephemdate):
    """ Converts pyephem date into POSIX unix time float (secs.ms since 1/1/1970) """
    return float(ephemdate.datetime().strftime("%s.%f"))

# tle update helpers
def update_tle_cb():
    print("%s: updating TLEs" % datetime.now())
    update_TLE()
    tle_update_timer = threading.Timer(TLE_UPDATE_PERIOD_S, update_tle_cb)
    tle_update_timer.setDaemon(True)
    tle_update_timer.start()

def stop_update_tle_daemon():
    if tle_update_timer is not None:
        tle_update_timer.cancel()
        tle_update_timer.join()

def start_update_tle_daemon():
    update_tle_cb()
    atexit.register(stop_update_tle_daemon)

if __name__ == '__main__':
    print("updating tle")
    update_TLE()
