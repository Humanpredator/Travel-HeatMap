import csv
import datetime
import json
import os


def make_reader(in_json):
    # Open location history data
    json_data = json.loads(open(in_json).read())

    # Get the easy fields
    for item in json_data['locations']:
        timestamp_str = item['timestamp']
        try:
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
        date = timestamp.strftime('%Y-%m-%d')
        timestamp = timestamp.strftime('%H:%M:%S')
        longitude = item['longitudeE7'] / 10000000.0
        latitude = item['latitudeE7'] / 10000000.0
        accuracy = item['accuracy']
        source = item['source']

        yield [date, timestamp, longitude, latitude, accuracy,source]


def getFullPath(inPath):
    if not os.path.isabs(inPath):
        # we need to set up the absolute path
        script_path = os.path.abspath(__file__)
        path, file = os.path.split(script_path)
        inPath = os.path.join(path, inPath)
    return inPath


# Read the Parameters
in_file = "Records.json"
out_file = "Records.csv"

in_file = getFullPath(in_file)
out_file = getFullPath(out_file)

features = [['Date', 'Time', 'Longitude', 'Latitude', 'Accuracy', 'Source']]
# add the Headers
print("Reading {0}".format(in_file))

reader = make_reader(in_file)

for r in reader:
    features.append(r)

print('Read {0} Records'.format(len(features)-1))

# write this data
with open(out_file, 'w', newline='')as f:
    writer = csv.writer(f)
    writer.writerows(features)