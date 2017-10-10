import track
import helpers
from flask import Flask
import json
from werkzeug.routing import FloatConverter as BaseFloatConverter

app = Flask(__name__)

class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

# Renew FloatConverter
app.url_map.converters['float'] = FloatConverter

sat_not_found = "404 - Satellite Not Found"
guide_path = './guide/index.html'

# API User Guide
@app.route('/api/')
def api_guide():
    with open(guide_path, 'r') as f:
        return f.read()

# Trackers
@app.route('/api/get_time')
def time():
    return track.Tracker().get_time()

@app.route('/api/get_velocity_vector/<string:s>')
def velocity_vector(s):
    return track.Tracker(s).get_velocity_vector()

@app.route('/api/get_velocity_vector')
def velocity_vector_default():
    return track.Tracker().get_velocity_vector()

@app.route('/api/get_velocity')
def velocity_default():
    return track.Tracker().get_velocity()

@app.route('/api/get_velocity/<string:s>')
def velocity(s):
    try:
        return track.Tracker(s).get_velocity()
    except KeyError:
        return sat_not_found

@app.route('/api/get_lonlatalt/<string:s>')
def lonlatalt(s):
    try:
        return track.Tracker(s).get_lonlatalt()
    except KeyError:
        return sat_not_found

@app.route('/api/get_lonlatalt')
def lonlatalt_default():
    return track.Tracker().get_lonlatalt()

# Observers
@app.route('/api/get_az_el/<string:s>/<float:lon>,<float:lat>,<float:alt>')
def az_el(lon, lat, alt, s):
    try:
        return track.Observer(sat = s, loc = (lon, lat, alt)).get_az_el()
    except KeyError:
        return sat_not_found

@app.route('/api/get_az_el/<float:lon>,<float:lat>,<float:alt>')
def az_el_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt)).get_az_el()

@app.route('/api/get_az_el/<string:s>')
def az_el_with_sat(s):
    try:
        return track.Observer(sat = s).get_az_el()
    except KeyError:
            return sat_not_found

@app.route('/api/get_az_el')
def az_el_default():
    return track.Observer().get_az_el()

@app.route('/api/get_next_pass/<string:s>/<float:lon>,<float:lat>,<float:alt>')
def next_pass(lon, lat, alt, s):
    try:
        return track.Observer(sat = s, loc = (lon, lat, alt)).get_next_pass()
    except KeyError:
            return sat_not_found

@app.route('/api/get_next_pass/<float:lon>,<float:lat>,<float:alt>')
def next_pass_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt)).get_next_pass()

@app.route('/api/get_next_pass/<string:s>')
def next_pass_with_sat(s):
    try:
        return track.Observer(sat = s).get_next_pass()
    except KeyError:
            return sat_not_found

@app.route('/api/get_next_pass')
def next_pass_default():
    return track.Observer().get_next_pass()

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 80)
