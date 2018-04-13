import csv
import matplot

with open ("data/huizen1.csv","r") as f:
    reader = csv.reader(f)
    houses = map(tuple, reader)

test_houses = [{ "location" : (1,2), "consumption" : 30},
               { "location" : (1,2), "consumption" : 29},
               { "location" : (9,5), "consumption" : 11},
               { "location" : (8,3), "consumption" : 28}]

battery = (3,2)

def manhattan(test_houses,battery):
    for house in test_houses:
        distance = 0
        for h,b in house["location"], battery:
            distance += abs(h - b)
        house["distance"] = distance

manhattan(test_houses, battery)
