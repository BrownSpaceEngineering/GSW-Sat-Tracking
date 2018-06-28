import track
import client
import helpers
from flask import Flask
import json
from werkzeug.routing import FloatConverter as BaseFloatConverter

api = Flask(__name__)

class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

# Renew FloatConverter
api.url_map.converters['float'] = FloatConverter

sat_not_found = "404 - Satellite Not Found"
guide_path = './docs/index.html'

# API User Guide
@api.route('/api')
def api_guide():
    with open(guide_path, 'r') as f:
        return f.read()

# Trackers
@api.route('/api/get_time')
def time():
    return track.Tracker().get_time()

@api.route('/api/get_orbit_number')
def get_orbit_number_default():
    return track.Tracker().get_orbit_number()

@api.route('/api/get_orbit_number/<string:s>')
def get_orbit_number_with_sat(s):
    return track.Tracker(s).get_orbit_number()

@api.route('/api/get_orbit_number/<string:s>/<float:hour>,<float:minute>,<float:second>')
def get_orbit_number_at_time(s, hour, minute, second):
    return track.Tracker(s).get_orbit_number(time = datetime.time(hour, minute, second))

@api.route('/api/get_next_passes/<string:s>/<float:length>/<float:hour>,<float:minute>,<float:second>/<float:lon>,<float:lat>,<float:alt>')
def get_next_passes(s, length, hour, minute, second, lon, lat, alt):
    return track.Tracker(s).get_next_passes(datetime.time(hour, minute, second), length, lon, lat, alt)

@api.route('/api/get_velocity_vector/<string:s>')
def velocity_vector(s):
    try:
    	return track.Tracker(s).get_velocity_vector()
    except KeyError:
    	return sat_not_found

@api.route('/api/get_velocity_vector')
def velocity_vector_default():
    return track.Tracker().get_velocity_vector()

@api.route('/api/get_velocity')
def velocity_default():
    return track.Tracker().get_velocity()

@api.route('/api/get_velocity/<string:s>')
def velocity(s):
    try:
        return track.Tracker(s).get_velocity()
    except KeyError:
        return sat_not_found

@api.route('/api/get_lonlatalt/<string:s>')
def lonlatalt(s):
    try:
        return track.Tracker(s).get_lonlatalt()
    except KeyError:
        return sat_not_found

@api.route('/api/get_lonlatalt')
def lonlatalt_default():
    return track.Tracker().get_lonlatalt()


@api.route('/api/get_lonlatalt_list/<string:s><float:starthour>,<float:startsecond>/<float:endhour>,<float:endsecond>/<float:interval>')
def lonlatalt_list(s, starthour, startsecond, endhour, endsecond, interval):
    # times are passed in as (hours, seconds) because datetime's timedelta
    # object does not allow for minutes.
    return track.Tracker(s).get_lonlatalt_list(datetime.timedelta(starthour, startsecond), datetime.timedelta(endhour, endsecond), interval)

# Observers
@api.route('/api/get_az_el/<string:s>/<float:lon>,<float:lat>,<float:alt>')
def az_el(lon, lat, alt, s):
    try:
        return track.Observer(sat = s, loc = (lon, lat, alt)).get_az_el()
    except KeyError:
        return sat_not_found

@api.route('/api/get_az_el/<float:lon>,<float:lat>,<float:alt>')
def az_el_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt)).get_az_el()

@api.route('/api/get_az_el/<string:s>')
def az_el_with_sat(s):
    try:
        return track.Observer(sat = s).get_az_el()
    except KeyError:
    	return sat_not_found

@api.route('/api/get_az_el')
def az_el_default():
    return track.Observer().get_az_el()

@api.route('/api/get_next_pass/<string:s>/<float:lon>,<float:lat>,<float:alt>')
def next_pass(lon, lat, alt, s):
    try:
        return track.Observer(sat = s, loc = (lon, lat, alt)).get_next_pass()
    except KeyError:
        return sat_not_found

@api.route('/api/get_next_pass/<float:lon>,<float:lat>,<float:alt>')
def next_pass_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt)).get_next_pass()

@api.route('/api/get_next_pass/<string:s>')
def next_pass_with_sat(s):
    try:
        return track.Observer(sat = s).get_next_pass()
    except KeyError:
        return sat_not_found

@api.route('/api/get_next_pass')
def next_pass_default():
    return track.Observer().get_next_pass()

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
    time = json.loads(track.Tracker().get_time())["current_time"]
    return json.dumps({"updated_time": time})

if __name__ == '__main__':
    api.run(debug = False, host = '0.0.0.0', port = 80)
