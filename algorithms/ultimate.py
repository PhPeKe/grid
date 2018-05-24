# minimale aantal kleinste batterijen berekenen
# batterijen plaatsen
# greedy + kmeans totdat t niet meer kan
# meest volle batterij upgraden
# etc
from classes.battery import Battery
from algorithms.kmeans import kmeans
from helpers.connectUnconnected import connectUnconnected
from helpers.visualize import visualize

from copy import deepcopy

def ultimate(district):

    capacities = [450, 900, 1800]
    batCosts = [900, 1350, 1800]
    totalOutput = 0
    for house in district.houses:
        totalOutput = totalOutput + house.output


    # initialize with set of low capacity batteries
    minNumBatteries = int(totalOutput / 450) + 1
    del district.batteries[:]
    distance = 50/minNumBatteries


    for i in range(minNumBatteries):
        battery = Battery(i * distance + distance / 2, 25, 450, i)
        battery.costs = 900
        district.batteries.append(battery)
    district.calculateCosts()

    district.connectGreedy()
    kmeans(district)

    costDifference = 1
    costDKmeans = 1

    while costDifference > 0:
        oldCosts = district.calculateCosts()
        while costDKmeans > 0:
            oldKCosts = district.calculateCosts()
            district.disconnect()
            district.connectGreedy()
            for uc in district.disconnectedHouses:
                connectUnconnected(uc, district.batteries)
            kmeans(district)
            print(district.costs, costDifference)
            costDKmeans = oldKCosts - district.calculateCosts()
            visualize(district)
            if district.costs < district.compare.costs and len(district.disconnectedHouses) == 0:
                district.compare = deepcopy(district)
            return

        # choose fullest battery to upgrade
        bats = district.batteries
        bats.sort(key=lambda x: x.capacity)
        district.disconnect()

        for b in bats:
            if b.capacity != capacities[len(capacities)-1]:
                index = capacities.index(b.capacity)
                b.capacity = capacities[index]
                b.costs = batCosts[index]
                break
        district.connectGreedy()

        for uc in district.disconnectedHouses:
            connectUnconnected(uc, district.batteries)
        kmeans(district)
        costDifference = oldCosts - district.calculateCosts()
        visualize(district)

        if district.costs < district.compare.costs and len(district.disconnectedHouses) == 0:
            district.compare = deepcopy(district)
        return


    district.calculateCosts()
    print("post ultimate costs:", district.costs)





