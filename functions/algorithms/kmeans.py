from copy import copy, deepcopy
from functions.visualize import visualize
def kmeans(district, numIt = 10, count = 0, contestants = []):


    print("      Price before", district.costs)
    if count > 0:
        district.disconnect()
        district.connectGreedy(True)

        while (district.allConnected == False):
            district.disconnect()
            district.connectGreedy(True)

    for b in district.batteries:
        meanLocation = [0,0]
        for h in b.connectedHouses:
            meanLocation[0] = meanLocation[0] + h.location[0]
            meanLocation[1] = meanLocation[1] + h.location[1]
        meanLocation[0] = round(meanLocation[0] / len(b.connectedHouses))
        meanLocation[1] = round(meanLocation[1] / len(b.connectedHouses))
        b.changeLocation(meanLocation)
        district.calculateCosts()

    print("kmeans iteration",count, str(district.costs))


    # Only the best
    contestants.append(deepcopy(district))
    contestants.sort(key = lambda x: x.costs)

    if district.costs <= contestants[0].costs:
        visualize(district, True, count)
        
    district = copy(contestants[0])

    if count < numIt:
        count += 1
        return kmeans(district, count = count, contestants = contestants, numIt = numIt)
    else:
        return district
