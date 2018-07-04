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
from twilio.rest import Client
import track
from math import sqrt
from collections import OrderedDict
import json
import ephem
from helpers import *
import csv
from collections import OrderedDict
import threading
from datetime import datetime
import time
import portalocker
import atexit

# Test credentials. These will not actually perform actions,
# but will display errors/success messages as if they had.
#account_sid = "AC1469c4fa6745ca1fd4ebba3f4953247e"
#auth_token = "4cbff2e61a6512ee87b658244f889843"
#gsw_num = "+15005550006"

# Real credentials:
account_sid = "AC81a035986f6be6decd80e773e934a0cd"
auth_token  = "112cf07ffc4eba703e60d3082f38253d"
gsw_num = "+19495183818"
client = Client(account_sid, auth_token)
fieldnames = ['number', 'lat', 'lon']

# Note that numbers must be in the format "+12345678". No parenthesis or dashes, 
# and we need the plus sign at the beginning.
class PhoneClient:
    
    # Open the phone database and check if it already contains the given number. 
    def get_loc_info(self, number):
        with open('phoneDB.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reversed(list(reader)):
                if row['number'] is number:
                    d = OrderedDict([
                        ('number', row['number']),
                        ('lon', row['lon']),
                        ('lat', row['lat'])
                    ])
                return json.dumps(d)

    # Write the number into the database. CURRENT BEHAVIOR: This will not actually
    # remove a client's old number from the database.
    def register_number(self, number, lat, lon):
        print("registering number")
        with open('phoneDB.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # We send a message to the number if it already exists in the database.
                # The current behavior has us still write the number with the new location
                # into the database, though.
                if row['number'] == number:
                    message = client.messages.create(to=number,from_=gsw_num,body="Warning, this number is already in the database.")
                    break
        # Add the information to the database.
        with open('phoneDB.csv', 'a') as f:
            #self.validate_new_number(number)

            # We put a write lock on the database, so that the Database Monitor can't 
            # read from the DB while we're writing a new number into it.
            portalocker.lock(f, portalocker.LOCK_EX)
            writer = csv.DictWriter(f, fieldnames=fieldnames)         
            writer.writerow({'number': number, 'lat': lat, 'lon':lon})   
            # and then unlock, and send a message to the client.
            portalocker.unlock(f)
            message = client.messages.create(to=number,from_=gsw_num,body="You're registered! We'll let you know when to look up!")
        return True

class DatabaseMonitor:
    
    def __init__(self):
        self.database_monitor_timer = None
    
    def send_sms(self, number):
        print("sending message to %s\n", number)
        message = client.messages.create(to=number,from_=gsw_num,body="The satellite's almost over your horizon. Keep your eyes peeled!")

    # Search database periodically to see if the satellite will be in sight of any of the locations within
    # the next five minutes.
    def search_database(self):
        with open('phoneDB.csv', 'r') as f:
            reader = csv.DictReader(f)
            # Because we don't currently remove numbers from the database, for now we read the database
            # from the bottom up, as the newer entries are on the bottom. For now.
            for row in reversed(list(reader)):
                pass_info = track.Observer(loc = (float(row['lon']), float(row['lat']), 0)).get_next_pass()
                pass_dictionary = json.loads(pass_info)
                rise_time = convert_unix_time_to_date(pass_dictionary['rise_time'])
                # note that rise_time should be in UTC time. We don't want to have half our numbers in local 
                # time and the other half in UTC.
                minutes_diff = (rise_time - datetime.utcnow()).total_seconds() / 60
                # If there's less than five minutes to go before the satellite's next pass, send the info
                if minutes_diff < 5:
                    send_sms(row['number']) 
        # Restart this again in five minutes.
        self.database_monitor_timer = threading.Timer(5*60*60, self.search_database)
        self.database_monitor_timer.setDaemon(True)
        self.database_monitor_timer.start()

    def stop_database_monitor(self):
        if self.database_monitor_timer is not None:   
            self.database_monitor_timer.cancel()
            self.database_monitor_timer.join()

    def start_database_monitor(self):
        self.search_database()
        atexit.register(self.stop_database_monitor)      

#PhoneClient().register_number("+15106763627", 15, 300)
#DatabaseMonitor().start_database_monitor()
