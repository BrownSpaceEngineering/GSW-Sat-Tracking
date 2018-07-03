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
<<<<<<< HEAD
import portalocker
import helpers
=======
import atexit
>>>>>>> newbranch

account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Your Auth Token from twilio.com/console
auth_token  = "your_auth_token"
gsw_num = "gswnumber"
client = Client(account_sid, auth_token)
fieldnames = ['number', 'lat', 'lon']
class PhoneClient:
    
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

    def register_number(self, number, lat, lon):
        with open('phoneDB.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['number'] == number:
                   # message = client.messages.create(to=number,from_=gsw_num,body="Warning, this number is already in the database.")
                    break

        with open('phoneDB.csv', 'a') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            writer = csv.DictWriter(f, fieldnames=fieldnames)         
            writer.writerow({'number': number, 'lat': lat, 'lon':lon})   
            portalocker.unlock(f)
            #message = client.messages.create(to=number,from_=gsw_num,body="Registered! We are tracking u")

        return True

class DatabaseMonitor:
    
    database_monitor_timer = None
    def send_sms(self, number):
        print("sending message to %s\n", number)
        #message = client.messages.create(to=number,from_=gsw_num,body="Satellite over horizon rn")

    def search_database(self):
        with open('phoneDB.csv', 'r') as f:
            reader = csv.DictReader(f)
            #We need to lock this file here
            for row in reversed(list(reader)):
                pass_info = track.Observer(loc = (float(row['lon']), float(row['lat']), 0)).get_next_pass()
                pass_dictionary = json.loads(pass_info)
                rise_time = convert_unix_time_to_date(pass_dictionary['rise_time'])
                minutes_diff = (rise_time - datetime.now()).total_seconds() / 60
                print(minutes_diff, row['number'])
                if minutes_diff < 5:
                    send_sms(row['number'])
        database_monitor_timer = threading.Timer(5, self.search_database)
        database_monitor_timer.setDaemon(True)
        database_monitor_timer.start()

    #def stop_database_monitor(self):
        #if database_monitor_timer is not None:   

    def start_database_monitor(self):
        self.search_database()
        #atexit.register(self.stop_database_monitor)      
        #t = threading.Thread(target=self.search_database)
        #t.start()

#DatabaseMonitor().start_database_monitor()
