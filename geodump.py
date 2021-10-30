import sqlite3
import json


conn = sqlite3.connect('geodata_2.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
with open('latlong.txt', 'w', encoding="utf-8") as fhand:
#fhand.write("myData = [\n")
    count = 0
    for row in cur :
        data = str(row[1].decode())
        try: js = json.loads(str(data))
        except: continue

        if not('status' in js and js['status'] == 'OK') : continue

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        if lat == 0 or lng == 0 : continue
        #where = js['results'][0]['formatted_address']
        #where = where.replace("'", "")
        try :
            print(lat, lng)

            count = count + 1
            if count > 1 : fhand.write("\n")
            output = str(lat) + "," + str(lng)
            fhand.write(output)
        except:
            continue

#fhand.write('\n')
cur.close()
fhand.close()
print(count, "records written to latlong.txt")
print("Open where.html to view the data in a browser")

