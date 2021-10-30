import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

API_KEY = True
# Need Google API key
API_KEY = input('Enter api key ')

key = API_KEY
serviceurl = "https://maps.googleapis.com/maps/api/elevation/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('elevationdata.sqlite') #connection to database; checks file access
cur = conn.cursor() #handle

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (locations TEXT, elevationdata TEXT)''') #cur.execute opens like a file

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("latlong.txt")
count = 0
for line in fh:
    if count > 12 :
        print('Retrieved 10 locations, restart to retrieve more')
        break

    locations = line.strip()
    print('')
    cur.execute("SELECT elevationdata FROM Locations WHERE locations= ?",
        (memoryview(locations.encode()), ))

    try:
        data = cur.fetchone()[0] #check if addess is already in the database, if so, skip
        print("Found in database ",locations)
        continue
    except:
        pass

    parms = dict()
    parms["locations"] = locations
    if API_KEY is not False: parms['key'] = API_KEY
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (locations, elevationdata)
            VALUES ( ?, ? )''', (memoryview(locations.encode()), memoryview(data.encode()) ) )
    conn.commit() #writes to disk
    #if count % 5 == 0 :
     #   print('Pausing for a bit...')
      #  time.sleep(5)

#print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
