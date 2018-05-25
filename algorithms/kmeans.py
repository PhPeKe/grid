from copy import copy, deepcopy
from random import shuffle
from helpers.compare import compare
from algorithms.hillclimber import hillclimbSwitcher
from helpers.visualize import visualize
from helpers.acceptanceProbability import acceptanceprobability
from random import random

def kmeans(district, numIt = 10, plot = False):
    """kmeans.

    Keyword arguments:
    district -- district object to apply kmeans on
    numIt    -- number of iterations to run
    plot     -- should plots be made? Can be "all" or "winner". In the second
                case only plots of the winning configurations (which are
                better than the ones before are made

    Flow:
    1. Batteries are centered to the middle of the houses connected to it
    2. The whole district is disconnected and reconnected in a random-greedy way
    3. Batteries are centered again and everything is repeated

    """
    count = 0
    miss = 0

    contestants = []
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
    """batteriesToMean.



    """
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

def checkConnections(district, count, contestants):
    # If Batteries already have been centered
    # the district is reconnected greedy
    if count > 0:
        district.disconnect()
        district.connectGreedy(True)
        c = 0
        # If the reconnection results in disconnected houses new attempts are
        # made until all houses are connected
        while (district.allConnected == False):
            for house in district.disconnectedHouses:
                hillclimbSwitcher(house, district, True)
                if len(district.disconnectedHouses) == 0:
                    return

            district.disconnect()
            # the first hundred times a greedy connection is tried
            if c < 100:
                district.connectGreedy(True)
                c += 1
            # If that doesnt work the district is reconnected random
            # to prevent an endless loop
            else:
                print("Connecting random")
                district.connectRandom()
                c += 1
                if c > 200:
                    print("random infinite")
                    district = contestants[0]
                    c = 0
