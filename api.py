import track
import helpers
from flask import Flask
app = Flask(__name__)

# API User Guide
@app.route('/api/')
def api_guide():
    return '<h1>API User Guide</h1>\n<p>This is the user guide</p>'

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

@app.route('/api/get_velocity/<string:s>')
def velocity(s):
    return track.Tracker(s).get_velocity()

@app.route('/api/get_velocity_vector')
def velocity_default():
    return track.Tracker().get_velocity()

@app.route('/api/get_lonlatalt/<string:s>')
def lonlatalt(s):
    return track.Tracker(s).get_lonlatalt()

@app.route('/api/get_lonlatalt')
def lonlatalt_default():
    return track.Tracker().get_lonlatalt()

# Observers
@app.route('/api/get_az_el/<string:s>/<int:lon>,<int:lat>,<int:alt>')
def az_el(lon, lat, alt, s):
    return track.Observer(sat = s, loc = (lon, lat, alt)).get_az_el()

@app.route('/api/get_az_el/<int:lon>,<int:lat>,<int:alt>')
def az_el_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt)).get_az_el()

@app.route('/api/get_az_el/<string:s>')
def az_el_with_sat(s):
    return track.Observer(sat = s).get_az_el()

@app.route('/api/get_az_el')
def az_el_default():
    return track.Observer().get_az_el()

@app.route('/api/get_next_pass/<string:s>/<int:lon>,<int:lat>,<int:alt>')
def next_pass(lon, lat, alt, s):
    return track.Observer(sat = s, loc = (lon, lat, alt)).get_next_pass()

@app.route('/api/get_next_pass/<int:lon>,<int:lat>,<int:alt>')
def next_pass_with_loc(lon, lat, alt):
    return track.Observer(loc = (lon, lat, alt)).get_next_pass()

@app.route('/api/get_next_pass/<string:s>')
def next_pass_with_sat(s):
    return track.Observer(sat = s).get_next_pass()

@app.route('/api/get_next_pass')
def next_pass_default():
    return track.Observer().get_next_pass()

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 80)
