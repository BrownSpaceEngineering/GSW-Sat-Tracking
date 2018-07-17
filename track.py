#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2017.

# Author(s):

#   Michael Mao <yicong_mao@brown.edu>
#   Kevin Du <kevin_du@brown.edu>
#   Purvi Goel <purvi_goel@brown.edu>
#   Trevor Houchens <trevor_houchens@brown.edu>
#   Andrew Wei <andrew_wei1@brown.edu>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Backend module for tracking EquiSat.
"""

from pyorbital import tlefile
from datetime import datetime, timedelta
from pyorbital.orbital import Orbital
from math import sqrt
from collections import OrderedDict
import math
import json
import ephem
from helpers import *

DEFAULT_SAT = "1998-067NY"
now = ephem.now()
class Tracker:
    _time = staticmethod(time)
    def_sat = DEFAULT_SAT

    def __init__(self, sat = def_sat, tle_file = DEFAULT_TLE_FILE):
        self.orb = get_orbital(sat, tle_file)

    def get_velocity_vector(self):
        normPos = self.orb.get_position(self._time(self), normalize=False)
        vel = normPos[1]
        d = OrderedDict([
            ('velocity_vector_x', vel[0]),
            ('velocity_vector_y', vel[1]),
            ('velocity_vector_z', vel[2])
        ])
        return json.dumps(d)

    def get_velocity(self):
        normPos = self.orb.get_position(self._time(self), normalize=False)
        vel = normPos[1]
        v = sqrt(sum(map(lambda x: x**2, vel)))
        d = {'velocity': v}
        return json.dumps(d)

    def get_lonlatalt(self):
        lonlatalt = self.orb.get_lonlatalt(self._time(self))
        d = OrderedDict([
            ('longitude', lonlatalt[0]),
            ('latitude', lonlatalt[1]),
            ('altitude', lonlatalt[2])
        ])
        return json.dumps(d)

    # takes in a startTime, which is a timeDelta object representing
    # the distance into the past we are starting at, and endTime,
    # a timeDelta object representing the distance into the future
    # we are searching until.
    def get_lonlatalt_list(self, startTime, endTime, interval):
        locationList = []
        # timedelta takes in (hours, seconds). Interval is the
        # number of seconds we increase by every time.
        tdelta = timedelta(0,interval)
        present = datetime.utcnow()
        # calculate the start and end points
        currTime = present - startTime
        finalTime = present + endTime
        while(currTime < finalTime):
            lonlatalt = self.orb.get_lonlatalt(currTime)
            currTime += tdelta
            d = OrderedDict([
                ('longitude', lonlatalt[0]),
                ('latitude', lonlatalt[1]),
                ('altitude', lonlatalt[2])
            ])
            currLocation = json.dumps(d)
            locationList.append(currLocation)
        return locationList

    def get_time(self):
        time = datetime.utcnow()
        d = {'current_time' : time.strftime('%Y-%m-%dT%H:%M:%S')}
        return json.dumps(d)

    def get_next_passes(self, time, length, lon, lat, alt):
        return self.orb.get_next_passes(time, length, lon, lat, alt)

    def get_orbit_number(self, time=datetime.utcnow()):
        return self.orb.get_orbit_number(time)

class Observer:
    _time = staticmethod(time)
    def_sat = DEFAULT_SAT
    status = True
    ip_loc, status = get_ip_loc()
    def __init__(self, sat = def_sat, loc = ip_loc, tle_file = DEFAULT_TLE_FILE):
        self.sat = sat
        self.orb = get_orbital(sat, tle_file)
        self.loc = loc
        if(self.loc == None):
            raise requests.exceptions.HTTPError
        self.tle_file = tle_file

    def get_az_el(self):
        loc = self.loc
        az_el = self.orb.get_observer_look(self._time(self), loc[0], loc[1], loc[2])
        d = OrderedDict([
            ('azimuth_angle', az_el[0]),
            ('elevation_angle', az_el[1])
        ])
        return json.dumps(d)

    def get_next_pass(self):
        passData = self.get_next_pass_data()
        # next_pass returns a six-element tuple giving:
        # (dates are in UTC)
        # 0  Rise time
        # 1  Rise azimuth
        # 2  Maximum altitude time
        # 3  Maximum altitude
        # 4  Set time
        # 5  Set azimuth
        # date info: http://rhodesmill.org/pyephem/date
        # next_pass info:
        # https://github.com/brandon-rhodes/pyephem/blob/592ecff661adb9c5cbed7437a23d705555d7ce57/libastro-3.7.7/riset_cir.c#L17        
        d = OrderedDict([
            ('rise_time', ephem_to_unix(passData[0])),
            ('rise_azimuth', math.degrees(passData[1])),
            ('max_alt_time', ephem_to_unix(passData[2])),
            ('max_alt', math.degrees(passData[3])),
            ('set_time', ephem_to_unix(passData[4])),
            ('set_azimuth', math.degrees(passData[5]))
        ])
        
        return d

    def get_next_pass_data(self):
        tle = get_TLE(self.sat)        
        sat = ephem.readtle(tle[0], tle[1], tle[2])
        obs = ephem.Observer()        
        lon, lat, el = self.loc
        obs.lon, obs.lat, obs.elevation = str(lon), str(lat), 0
        passData = obs.next_pass(sat)    
        return passData

if __name__ == "__main__":
    t = Tracker()
    o = Observer(sat="ISS (ZARYA)", loc=(-71.3991,41.8391,0))
    d = o.get_next_pass()
    print(d)
    #print(t.get_time(), t.get_velocity_vector(), t.get_velocity(), t.get_lonlatalt(), o.get_az_el(), o.get_next_pass(), sep="\n")
