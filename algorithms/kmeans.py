from copy import copy, deepcopy
from random import shuffle
from helpers.compare import compare
from algorithms.hillclimber import hillclimbSwitcher
from helpers.visualize import visualize
def kmeans(district, numIt = 10, count = 0, contestants = [], miss = 0, plot = False):
    temp = district.mode
    district.mode += "kmeans"
    temperature = 1
    while (count < numIt):

        print("       Price before: ", district.costs)
        checkConnections(district, count, contestants)
        batteriesToMean(district)
        #compare(district)
        print("kmeans iteration: ",count, str(district.costs))


        # Only the best
        contestants.append(deepcopy(district))
        contestants.sort(key = lambda x: x.costs)
        if plot == "all":
            visualize(district, True, count)
        if district.costs <= contestants[0].costs:
            if plot == "winner":
                visualize(district, True, count)
        else:
            miss += 1
            # RESEARCH:
            # /10 and /5 works better than /20 and /10:
            # Finds (local) optimum pretty fast:
            # +- 200 iterations
            if miss > numIt /10:
                shuffle(contestants)
                if miss > numIt / 5:
                    miss = 0
                    district.disconnect()
                    district.connectRandom()
        district = deepcopy(contestants[0])
        count += 1

    contestants.sort(key = lambda x: x.costs)
    district = contestants[0]

    district.mode = temp
    return district



def batteriesToMean(district):
    # Set battery to mean location
    for b in district.batteries:
        meanLocation = [0,0]
        for h in b.connectedHouses:
            meanLocation[0] = meanLocation[0] + h.location[0]
            meanLocation[1] = meanLocation[1] + h.location[1]
        if not len(b.connectedHouses) == 0:
            meanLocation[0] = round(meanLocation[0] / len(b.connectedHouses))
            meanLocation[1] = round(meanLocation[1] / len(b.connectedHouses))
        else:
            meanLocation = [0,0]
        b.changeLocation(meanLocation)
        district.calculateCosts()

def checkConnections(district, contestants):
    # If Batteries already have been centered
    # the district is reconnected greedy
    district.disconnect()
    district.connectGreedy(True)
    c = 0
    temperature = 250
    coolingRate = 0.95
    # If the reconnection results in disconnected houses new attempts are
    # made until all houses are connected
    while (district.allConnected == False):
        for house in district.disconnectedHouses:
            hillclimbSwitcher(house, district, True)
            if len(district.disconnectedHouses) == 0:
                return
        if acceptanceprobability(district.costs, contestants[0].costs, temperature) < random():
            district.disconnect()
            district.connectGreedy(True)
        else:
            district.disconnect()
            district.connectRandom()
        temperature *= coolingRate
        c += 1
        if c > 1000:
            print("Endless loop?")
            district = deepcopy(contestants[0])
            break
