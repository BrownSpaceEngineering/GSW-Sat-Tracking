from pyorbital import tlefile
from datetime import datetime
from pyorbital.orbital import Orbital
from getLocation import getLoc
from math import sqrt
import json

import ephem

from flask import Flask 
from flask_restful import Resource, Api, reqparse
from nextPass import *
from satTrack import *



app = Flask(__name__)
api = Api(app)

class getVelocity(Resource):
	def get(self):
		return getVelocity()

api.add_resource(getVelocity, '/')
