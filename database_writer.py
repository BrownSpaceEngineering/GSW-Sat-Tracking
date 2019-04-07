#!/usr/bin/python
import csv
import sqlite3

conn = sqlite3.connect('phoneDb.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE phones
             (number text, lat text, lon text)''')

# Insert a row of data
c.execute("INSERT INTO phones VALUES ('+12345','1','2')")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()