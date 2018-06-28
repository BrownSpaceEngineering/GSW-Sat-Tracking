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

    # is location lon lat alt or lat lon alt
    def register_number(self, number, lat, lon):
        with open('phoneDB.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['number'] == number:
                   # message = client.messages.create(to=number,from_=gsw_num,body="Warning, this number is already in the database.")
                    break

        with open('phoneDB.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)         
            writer.writerow({'number': number, 'lat': lat, 'lon':lon})   
            #message = client.messages.create(to=number,from_=gsw_num,body="Registered! We are tracking u fam. reply STOP and we wont stalk")

        return True

class DatabaseMonitor:

    def send_sms(self, number):
        print("sending message to %s\n", number)
        #message = client.messages.create(to=number,from_=gsw_num,body="Satellite incoming i love science")

    def search_database(self):
        print("Search db")
        while True:
            with open('phoneDB.csv', 'r') as f:
                reader = csv.DictReader(f)
                #lock file
                for row in reversed(list(reader)):
                    #sat = 'ISS (ZARYA)', loc = (int(row['lon']), int(row['lat']), 0)
                    pass_info = track.Observer(loc = (int(row['lon']), int(row['lat']), 0)).get_next_pass()
                    pass_dictionary = json.loads(pass_info)
                    ephem_date = convert_ephem_float_to_date(pass_dictionary['rise_time'])
                    rise_time = datetime.strptime(str(ephem_date), "%Y/%m/%d %H:%M:%S")
                    minutes_diff = (rise_time - datetime.now()).total_seconds() / 60
                    print(minutes_diff)
                    if minutes_diff < 5:
                        send_sms(row['number'])
            time.sleep(10)

    def start_timer(self):
        t = threading.Thread(target=self.search_database)
        t.start()


DatabaseMonitor().start_timer();

#PhoneClient().register_number(1,5,4)
#print(PhoneClient().get_loc_info("1"))