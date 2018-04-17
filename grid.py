import csv
from classes.classes import *

# Open csv and txt file
with open("data/wijk1_huizen.csv","r") as f:
    reader = csv.reader(f)
    houses_raw = list(reader)

with open("data/wijk1_batterijen.txt") as f:
    reader = csv.reader(f, delimiter="\t")
    batteries_raw = list(reader)

# Convert list of houses to dictionary
houses = []

# [1:] to ignore header
for count, house in enumerate(houses_raw[1:]):
    houses.append(House(int(house[0]),
                        int(house[1]),
                        float(house[2]),
                        int(count)))

targetList = []

# Skip empty entries because of inconsistent file format
for battery in batteries_raw[1:]:
    tl = []
    for entry in battery:
        if entry:
            tl.append(entry)
    targetList.append(tl)
batteries_raw = targetList

batteries = []
for count, battery in enumerate(batteries_raw):
    battery[0] = battery[0].strip("[] ").split(", ")
    batteries.append(Battery(int(battery[0][0]),
                             int(battery[0][1]),
                             float(battery[1]),
                             int(count)))

# Calculate the manhattan distance
def manhattan(house,battery):
    distance = 0
    for h,b in house["location"], battery["location"]:
        distance += abs(h - b)
    #house["distance"] = distance
    return(distance)



#for h in houses:
#    for b in batteries:
#        print(manhattan(h,b), h["distance"])
#        if manhattan(h,b) < h["distance"]:
#            h["distance"] = int(manhattan(h,b))
#            h["connected to"] = b["id"]
