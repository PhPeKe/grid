import csv

# Open csv and txt file
with open("data/wijk1_huizen.csv","r") as f:
    reader = csv.reader(f)
    houses = list(reader)

with open("data/wijk1_batterijen.txt") as f:
    reader = csv.reader(f, delimiter="\t")
    batteries = list(reader)

# Convert list of houses to dictionary
targetList = []

# [1:] to ignore header
for count, house in enumerate(houses[1:]):
    targetList.append({"location" : (int(house[0]),int(house[1])),
                        houses[0][2] : float(house[2]),
                        "id" : count})
houses = targetList

targetList = []

for battery in batteries[1:]:
    tl = []
    for entry in battery:
        if entry:
            tl.append(entry)
    targetList.append(tl)
batteries = targetList

targetList = []
for count, battery in enumerate(batteries):
    battery[0] = battery[0].strip("[] ").split(", ")
    targetList.append({"location" : (int(battery[0][0]),int(battery[0][1])),
                       "capacity" : float(battery[1]),
                       "id" : count})
batteries = targetList

# Calculate the manhattan distance
def manhattan(house,battery):
    distance = 0
    for h,b in house["location"], battery["location"]:
        distance += abs(h - b)
    #house["distance"] = distance
    return(distance)

# Large default distance
for house in houses:
    house["distance"] = 100000

for h in houses:
    for b in batteries:
        print(manhattan(h,b), h["distance"])
        if manhattan(h,b) < h["distance"]:
            h["distance"] = int(manhattan(h,b))
            h["connected to"] = b["id"]
