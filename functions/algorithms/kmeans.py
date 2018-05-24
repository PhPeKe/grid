from copy import copy, deepcopy
from functions.visualize import visualize
from random import shuffle
def kmeans(district, numIt = 10, count = 0, contestants = [], miss = 0, plotIndex = None):


    print("       Price before: ", district.costs)
    if count > 0:
        district.disconnect()
        district.connectGreedy(True)
        c = 0
        while (district.allConnected == False):
            district.disconnect()
            if c > 100:
                print("Connecting random")
                district.connectRandom()
                c = 0
            else:
                district.connectGreedy(True)
                c += 1

    # Set battery to mean location
    for b in district.batteries:
        meanLocation = [0,0]
        for h in b.connectedHouses:
            meanLocation[0] = meanLocation[0] + h.location[0]
            meanLocation[1] = meanLocation[1] + h.location[1]
        meanLocation[0] = round(meanLocation[0] / len(b.connectedHouses))
        meanLocation[1] = round(meanLocation[1] / len(b.connectedHouses))
        b.changeLocation(meanLocation)
        district.calculateCosts()

    print("kmeans iteration: ",count, str(district.costs))


    # Only the best
    contestants.append(deepcopy(district))
    contestants.sort(key = lambda x: x.costs)
    visualize(district, True, plotIndex)
    #visualize(district, True, count)
    if district.costs <= contestants[0].costs:
        #visualize(district, True, plotIndex)
        a = 0
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


    district = copy(contestants[0])

    if count < numIt:
        plotIndex += 1
        count += 1
        return kmeans(district,
                      count = count,
                      contestants = contestants,
                      numIt = numIt,
                      miss = miss,
                      plotIndex = plotIndex)
    else:
        contestants.sort(key = lambda x: x.costs)
        return district, plotIndex
