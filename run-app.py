import satTrack
from flask import Flask
app = Flask(__name__)

@app.route('/api')
def hello_world():
    return 'Flask running'

@app.route('/api/dummy')
def dummy():
    return satTrack.getTime()

@app.route('/api//<some_location>')
def

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
