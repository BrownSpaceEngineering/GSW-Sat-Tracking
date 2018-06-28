#!/usr/bin/python
import csv
 
with open('phoneDb.csv', 'w') as csvfile:
    fieldnames = ['number', 'lat', 'lon']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
 
    writer.writeheader()
 
print("writing complete")