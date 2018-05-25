from classes.battery import Battery
from algorithms.kmeans import kmeans
from algorithms.hillclimber import hillclimbSwitcher
from helpers.visualize import visualize
from copy import deepcopy
from helpers.acceptanceProbability import acceptanceprobability
from random import random



def ultimate(district):
    print("ULTIMATE")

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
    kmeans(district, 3)

    costDifference = 1
    costDKmeans = 1
    temperature = 250
    coolingRate = 0.95

    while costDifference > 0:
        oldCosts = district.calculateCosts()
        while costDKmeans> 0:
            district = kmeans(district, 3)

            district.calculateCosts()
            costDKmeans = oldCosts - district.costs
            oldCosts = district.calculateCosts()
            district.save("ultimate.txt")
            #if acceptanceprobability(district.calculateCosts(), oldCosts, temperature) > random()

        print("-----BATTERY UPGRADE----")
        batteryUpgrade(district, capacities, batCosts, oldCosts, costDifference)


    district.calculateCosts()
    print("post ultimate costs:", district.costs)


def batteryUpgrade(district, capacities, batCosts, oldCosts, costDifference):
    # choose fullest battery to upgrade
    bats = district.batteries
    bats.sort(key=lambda x: x.capacity)
    district.disconnect()

    for b in bats:
        if b.capacity != capacities[len(capacities) - 1]:
            index = capacities.index(b.capacity)
            b.capacity = capacities[index]
            b.costs = batCosts[index]
            b.maxCapacity = capacities[index]
            print(b.id, b.location)
            break
    district.connectGreedy()

    toBeRemoved = bats[len(bats)-1]
    print(toBeRemoved.id)
    district.batteries.remove(bats[len(bats)-1])
    for b in bats:
        print(b.id, b.location)
    print("len ultimate",len(district.batteries))

    for i in range(len(district.batteries)):
        district.batteries[i].id = i
    visualize(district)

    district.connectGreedy()

    for uc in district.disconnectedHouses:
        hillclimbSwitcher(uc, district, True)
    print("new number of batteries: ", len(district.batteries))

    for house in district.disconnectedHouses:
        hillclimbSwitcher(house, district, True)


    if len(district.disconnectedHouses) != 0:
        district.batteries.append(toBeRemoved)

    district = kmeans(district)
    visualize(district)
    district.compare

