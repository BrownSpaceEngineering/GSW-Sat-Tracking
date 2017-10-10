#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2017.

# Author(s):

#   Michael Mao <yicong_mao@brown.edu>

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
from datetime import datetime
from pyorbital.orbital import Orbital
from math import sqrt
from collections import OrderedDict
import json
import ephem
from helpers import *

class Tracker:
    _time = staticmethod(time)
    def_sat = 'ISS (ZARYA)'

    def __init__(self, sat = def_sat):
        self.orb = get_orbital(sat)

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

    def get_time(self):
        time = datetime.utcnow()
        d = {'current_time' : time.strftime('%Y-%m-%dT%H:%M:%S')}
        return json.dumps(d)

class Observer:
    _time = staticmethod(time)
    def_sat = 'ISS (ZARYA)'
    ip_loc = get_ip_loc()

    def __init__(self, sat = def_sat, loc = ip_loc):
        self.sat = sat
        self.orb = get_orbital(sat)
        self.loc = loc

    def get_az_el(self):
        loc = self.loc
        az_el = self.orb.get_observer_look(self._time(self), loc[0], loc[1], loc[2])
        d = OrderedDict([
            ('azimuth_angle', az_el[0]),
            ('elevation_angle', az_el[1])
        ])
        return json.dumps(d)

    def get_next_pass(self):
        tle = get_TLE(self.sat)
        sat = ephem.readtle(tle[0], tle[1], tle[2])
        obs = ephem.Observer()
        obs.lon, obs.lat, obs.elevation = self.loc
        passData = obs.next_pass(sat)
        # next_pass returns a six-element tuple giving:
        # 0  Rise time
        # 1  Rise azimuth
        # 2  Maximum altitude time
        # 3  Maximum altitude
        # 4  Set time
        # 5  Set azimuth
        d = OrderedDict([
            ('rise_time', passData[0]),
            ('rise_azimuth', passData[1]),
            ('max_alt_time', passData[2]),
            ('max_alt', passData[3]),
            ('set_time', passData[4]),
            ('set_azimuth', passData[5])
        ])
        return json.dumps(d)

if __name__ == "__main__":
    t = Tracker()
    o = Observer()
    print(t.get_time(), t.get_velocity_vector(), t.get_velocity(), t.get_lonlatalt(),
        o.get_az_el(), o.get_next_pass(), sep = "\n")
