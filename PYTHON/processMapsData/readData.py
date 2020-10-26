import json
import datetime

# set folders and files
dataFolder = "../../DATA/"
fileName = "googlePositions.json"

# load json data
with open(dataFolder + fileName) as f:
  data = json.load(f)

# loop through all locations
loc_date_prev = ""
num_dates = 0
for loc in data["locations"]:
    # get time of location
    loc_ts = int(int(loc["timestampMs"]) / 1000)
    loc_datetime = datetime.datetime.fromtimestamp(loc_ts)
    loc_date = loc_datetime.strftime("%d-%m-%Y")

    if(loc_date != loc_date_prev) :
        num_dates = num_dates + 1
        print(loc_date)

    loc_date_prev = loc_date

print(num_dates)
