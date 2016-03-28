#!/usr/bin/python

#================================================================================#
#                             ADS-B FEEDER PORTAL                                #
# ------------------------------------------------------------------------------ #
# Copyright and Licensing Information:                                           #
#                                                                                #
# The MIT License (MIT)                                                          #
#                                                                                #
# Copyright (c) 2015-2016 Joseph A. Prochazka                                    #
#                                                                                #
# Permission is hereby granted, free of charge, to any person obtaining a copy   #
# of this software and associated documentation files (the "Software"), to deal  #
# in the Software without restriction, including without limitation the rights   #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
# copies of the Software, and to permit persons to whom the Software is          #
# furnished to do so, subject to the following conditions:                       #
#                                                                                #
# The above copyright notice and this permission notice shall be included in all #
# copies or substantial portions of the Software.                                #
#                                                                                #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  #
# SOFTWARE.                                                                      #
#================================================================================#

# WHAT THIS DOES:                                                 
# ---------------------------------------------------------------
#
# 1) Read aircraft.json generated by dump1090-mutability.
# 2) Add the flight to the database if it does not already exist.
# 3) Update the last time the flight was seen.
#
# REQUIRED PACKAGES:
# ---------------------------------------------------------------
# python-mysqldb


import datetime
import json
import MySQLdb
import sqlite3
import time

#import urllib2

while True:

    # Read dump1090-mutability's aircraft.json.
    with open('/run/dump1090-mutability/aircraft.json') as data_file:
        data = json.load(data_file)
    # For testing using a remote JSON feed.
    #response = urllib2.urlopen('http://xxx.xxxxxx.xxx/dump1090/data/aircraft.json')
    #data = json.load(response)

    ## Connect to a MySQL database.
    db = MySQLdb.connect(host="localhost", user="adsbuser", passwd="password", db="adsb")

    ## Connect to a SQLite database.
    #db = sqlite3.connect("/var/www/html/data/portal.sqlite")

    cursor = db.cursor()
    for aircraft in data["aircraft"]:
        # Make sure flight is specified.
        if aircraft.has_key('flight'):
            # Check to see if the flight already exists in the database.
            cursor.execute("SELECT COUNT(*) FROM adsb_flights WHERE flight = '" + aircraft["flight"].strip() + "'")
            row_count = cursor.fetchone()
            if row_count[0] == 0:
                print("Adding Flight: " + aircraft["flight"].strip())
                # If the flight does not exist in the database add it.
                cursor.execute("INSERT INTO adsb_flights (flight) VALUES ('" + aircraft["flight"] + "')")
            # Update the time it was last seen.
            cursor.execute("UPDATE adsb_flights SET lastSeen = '" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "' WHERE flight = '" + aircraft["flight"] + "'")
    # Close the database connection.
    db.commit()
    db.close()

    print("Last Run: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ".") 
    time.sleep(5)
