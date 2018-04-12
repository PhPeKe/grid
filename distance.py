houses = [{ "location" : (1,2), "distance" : [], "consumption" : 30},
          { "location" : (1,2), "distance" : [], "consumption" : 29},
          { "location" : (9,5), "distance" : [], "consumption" : 11},
          { "location" : (8,3), "distance" : [], "consumption" : 28}]
battery = (3,2)
distances = []

def manhattan(houses,battery):
    for house in houses:
        distance = 0
        for h,b in house["location"], battery:
            distance += abs(h - b)

        house["distance"] = distance

manhattan(houses, battery)
