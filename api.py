import track
import client
import datetime
import helpers
from flask import Flask, jsonify, send_from_directory
import json
from helpers import DEFAULT_TLE_FILE
from werkzeug.routing import FloatConverter as BaseFloatConverter

api = Flask(__name__, static_folder="./")

class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

# Renew FloatConverter
api.url_map.converters['float'] = FloatConverter

sat_not_found = "404 - Satellite Not Found"
guide_path = './docs/index.html'

# tle file customization. Static file will not be auto-updated, default will be.
USE_STATIC_TLE_FILE = False
STATIC_TLE_FILE = "equisat-tle.txt"
TLE_FILE = STATIC_TLE_FILE if USE_STATIC_TLE_FILE else DEFAULT_TLE_FILE

# API User Guide
@api.route('/api')
def api_guide():
    return send_from_directory("docs", "index.html")

# Trackers
@api.route('/api/tle')
@api.route('/api/Amateur.tle')
def equisat_tle():
    return api.send_static_file(TLE_FILE)

@api.route('/api/get_time')
def time():
    return track.Tracker(tle_file = TLE_FILE).get_time()

@api.route('/api/get_orbit_number')
def get_orbit_number_default():
    return track.Tracker(tle_file = TLE_FILE).get_orbit_number()

@api.route('/api/get_orbit_number/<string:s>')
def get_orbit_number_with_sat(s):
    return track.Tracker(s, tle_file = TLE_FILE).get_orbit_number()

@api.route('/api/get_orbit_number/<string:s>/<float:hour>,<float:minute>,<float:second>')
def get_orbit_number_at_time(s, hour, minute, second):
    return track.Tracker(s, tle_file = TLE_FILE).get_orbit_number(time = datetime.time(hour, minute, second))

@api.route('/api/get_next_passes/<string:s>/<int:length>/<float:lon>,<float:lat>,<float:alt>')
def get_next_passes(s, length, lon, lat, alt):
    dtime = datetime.datetime.now()
    pass_times = track.Tracker(s, tle_file = TLE_FILE).get_next_passes(dtime, length, lon, lat, alt)
    posix_times = []
    for dtime in pass_times:
        posix_times.append(float(dtime.strftime("%s.%f")))
    return jsonify(posix_times)

@api.route('/api/get_velocity_vector/<string:s>')
def velocity_vector(s):
    try:
    	return track.Tracker(s, tle_file = TLE_FILE).get_velocity_vector()
    except KeyError:
    	return sat_not_found

@api.route('/api/get_velocity_vector')
def velocity_vector_default():
    return track.Tracker(tle_file = TLE_FILE).get_velocity_vector()

@api.route('/api/get_velocity')
def velocity_default():
    return track.Tracker(tle_file = TLE_FILE).get_velocity()

@api.route('/api/get_velocity/<string:s>')
def velocity(s):
    try:
        return track.Tracker(s, tle_file = TLE_FILE).get_velocity()
    except KeyError:
        return sat_not_found

@api.route('/api/get_lonlatalt/<string:s>')
def lonlatalt(s):
    try:
        return track.Tracker(s, tle_file = TLE_FILE).get_lonlatalt()
    except KeyError:
        return sat_not_found

@api.route('/api/get_lonlatalt')
def lonlatalt_default():
    return track.Tracker(tle_file = TLE_FILE).get_lonlatalt()


@api.route('/api/get_lonlatalt_list/<string:s>/<float:starthour>,<float:startsecond>/<float:endhour>,<float:endsecond>/<float:interval>')
def lonlatalt_list(s, starthour, startsecond, endhour, endsecond, interval):
    # times are passed in as (hours, seconds) because datetime's timedelta
    # object does not allow for minutes.
    list_of_json = track.Tracker(s, tle_file = TLE_FILE).get_lonlatalt_list(datetime.timedelta(starthour, startsecond), datetime.timedelta(endhour, endsecond), interval)
    full_string = "["
    for elm in list_of_json:
        full_string += elm + ","
    return full_string[:len(full_string)-1] + "]" # remove ","

# Observers
@api.route('/api/get_az_el/<string:s>/<float:lon>,<float:lat>,<float:alt>')
def az_el(lon, lat, alt, s):
    try:
        return track.Observer(sat = s, loc = (lon, lat, alt), tle_file = TLE_FILE).get_az_el()
    except KeyError:
        return sat_not_found

@api.route('/api/get_az_el/<float:lon>,<float:lat>,<float:alt>')
def az_el_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt), tle_file = TLE_FILE).get_az_el()

@api.route('/api/get_az_el/<string:s>')
def az_el_with_sat(s):
    try:
        return track.Observer(sat = s, tle_file = TLE_FILE).get_az_el()
    except KeyError:
    	return sat_not_found

@api.route('/api/get_az_el')
def az_el_default():
    return track.Observer(tle_file = TLE_FILE).get_az_el()

@api.route('/api/get_next_pass/<string:s>/<float:lon>,<float:lat>,<float:alt>')
def next_pass(lon, lat, alt, s):
    try:
        return track.Observer(sat = s, loc = (lon, lat, alt), tle_file = TLE_FILE).get_next_pass()
    except KeyError:
        return sat_not_found

@api.route('/api/get_next_pass/<float:lon>,<float:lat>,<float:alt>')
def next_pass_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt), tle_file = TLE_FILE).get_next_pass()

@api.route('/api/get_next_pass/<string:s>')
def next_pass_with_sat(s):
    try:
        return track.Observer(sat = s, tle_file = TLE_FILE).get_next_pass()
    except KeyError:
        return sat_not_found

@api.route('/api/get_next_pass')
def next_pass_default():
    return track.Observer(tle_file = TLE_FILE).get_next_pass()

@api.route('/api/number_exists/<string:number>')
def number_exists(number):
    return client.get_loc_info(number)

@api.route('/api/register/<string:number>,<float:lat>,<float:lon>')
def register_phone(number,lat,lon):
    return client.register_phone(number, lat, lon)

# Maual maintenance
@api.route('/api/update')
def update_tle():
    helpers.update_TLE()
    time = json.loads(track.Tracker(tle_file = DEFAULT_TLE_FILE).get_time())["current_time"]
    return json.dumps({"updated_time": time})

if __name__ == '__main__':
    helpers.start_update_tle_daemon()
    api.run(debug = False, host = '0.0.0.0', port = 80)
