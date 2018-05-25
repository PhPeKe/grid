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
    # Initialize counting variables and list with all attempts
    count = 0
    miss = 0
    contestants = []

    while (count < numIt):
        print("       Price before: ", district.costs)
        checkConnections(district, count, contestants)
        batteriesToMean(district)
        #compare(district)
        print("kmeans iteration: ",count, str(district.costs))


        # Keep all "contestants"
        contestants.append(deepcopy(district))

        # Sort them to select the best later by default
        contestants.sort(key = lambda x: x.costs)

        # Make plots if it is wished
        if plot == "all":
            visualize(district, True, count)

        if district.costs <= contestants[0].costs:
            if plot == "winner":
                visualize(district, True, count)

        # If the solutionis not better than the best so far its a miss
        else:
            miss += 1
            # If there are more misses in a row than 10% of the number of
            # iterations the list is shuffled so that later a random contestant
            # is chosen for the next iteration
            if miss > numIt /10:
                shuffle(contestants)
                # If this still does not yield better results in 20% of the
                # number of iterations the district is randomly reconncted
                if miss > numIt / 5:
                    miss = 0
                    district.disconnect()
                    district.connectRandom()

        # Here the district for the next iteration is chosen
        district = deepcopy(contestants[0])
        count += 1

    # return the best configuration
    contestants.sort(key = lambda x: x.costs)
    district = contestants[0]
    return district



def batteriesToMean(district):
    """batteriesToMean.

    Centers batteries:
    1. Calculate mean location of connectedHouses
    2. Moves batteries to center
    3. Updates costs

    """
    # Set battery to mean location
    for b in district.batteries:
        meanLocation = [0,0]
        # Get mean location
        for h in b.connectedHouses:
            meanLocation[0] = meanLocation[0] + h.location[0]
            meanLocation[1] = meanLocation[1] + h.location[1]
        if not len(b.connectedHouses) == 0:
            meanLocation[0] = round(meanLocation[0] / len(b.connectedHouses))
            meanLocation[1] = round(meanLocation[1] / len(b.connectedHouses))
        else:
            meanLocation = [0,0]
        # Set mean location and updte costs
        b.changeLocation(meanLocation)
        district.calculateCosts()

def checkConnections(district, count, contestants):
    """check connections

    Disconnects and reconnects district.
    1. Disconnects district
    2. Reconnects greedy:
        If reconnecting greedy is not possible because it leaves some houses
        unconnected a while loop is used to reconnect everything.
    3. If reconnecting greedy doesnt work random connections are made because
       they are more likely to yield a valid connection where no houses are
       unconnected.

    """
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
