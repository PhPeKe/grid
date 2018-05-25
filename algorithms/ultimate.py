# minimale aantal kleinste batterijen berekenen
# batterijen plaatsen
# greedy + kmeans totdat t niet meer kan
# meest volle batterij upgraden
# etc
from classes.battery import Battery
from algorithms.kmeans import kmeans
from algorithms.hillclimber import hillclimbSwitcher
from helpers.visualize import visualize
from copy import deepcopy
from helpers.acceptanceProbability import acceptanceprobability
from random import random

from copy import copy


def ultimate(district):
    print("ULTIMATE")
    district.mode = "ultimate-"
    x = 0
    capacities = [450, 900, 1800]
    batCosts = [900, 1350, 1800]
    totalOutput = 0
    for house in district.houses:
        totalOutput = totalOutput + house.output

    # initialize with set of low capacity batteries
    minNumBatteries = int(totalOutput / 450) + 1
    del district.batteries[:]
    distance = 50/minNumBatteries

    district.disconnect()
    for i in range(minNumBatteries):
        battery = Battery(i * distance + distance / 2, 25, 450, i)
        battery.costs = 900
        battery.batteryType = 0
        district.batteries.append(battery)
    district.calculateCosts()

    district.connectGreedy()
    district = kmeans(district)

    costDifference = 1
    costDKmeans = 1
    temperatute = 250
    coolingRate = 0.95
    count = 0
    numIt = 10
    while True:#costDifference > 0:
        oldCosts = copy(district.calculateCosts())
        while costDKmeans > 0:
            oldCosts = copy(district.calculateCosts())
            print(" while it")
            district = kmeans(district, numIt = 3)
           ##visualize(district, True, district.mode + str(x))
            x += 1
            district.calculateCosts()
            costDKmeans = oldCosts - district.costs
        count += 1
        batteryUpgrade(district, capacities, batCosts, oldCosts, costDifference)
        if acceptanceprobability(district.calculateCosts(), oldCosts, temperatute) < random():
            break
        temperatute *= coolingRate
        costDKmeans = 1

    district.calculateCosts()
    print("post ultimate costs:", district.costs)


def batteryUpgrade(district, capacities, batCosts, oldCosts, costDifference):

    #visualize(district, False, "Before joining")
    #district.disconnect()
    upgradeBattery = None
    joinClosestBatteries(district, batCosts)
    #visualize(district)
    return


def joinClosestBatteries(district, batCosts):
    district.setClosestBattery()
    district.batteries.sort(key = lambda x: x.closestBatteryDistance)
    closestBatteries = [district.batteries[0], district.batteries[0].closestBattery]

    if closestBatteries[0].batteryType != 2 and closestBatteries[1].batteryType != 2:
        usedCapacity0 = closestBatteries[0].maxCapacity - closestBatteries[0].capacity
        usedCapacity1 = closestBatteries[1].maxCapacity-closestBatteries[1].capacity
        print(usedCapacity1, usedCapacity0, closestBatteries[0].maxCapacity * 2)


        if (usedCapacity0 + usedCapacity1) <= (closestBatteries[0].maxCapacity * 2):
            closestBatteries[0].maxCapacity *= 2
            closestBatteries[0].batteryType += 1
            closestBatteries[0].costs = batCosts[closestBatteries[0].batteryType]
            closestBatteries[0].capacity += closestBatteries[1].capacity

            for house in closestBatteries[1].connectedHouses:
                closestBatteries[0].connectedHouses.append(house)
                house.connection = closestBatteries[0]
            district.batteries.remove(closestBatteries[1])
            for i in range(len(district.batteries)):
                district.batteries[i].id = i

            kmeans(district, numIt=1)
    return district

def OLDbatteryUpgrade(district, capacities, batCosts):
    # choose fullest battery to upgrade
    bats = district.batteries
    bats.sort(key=lambda x: x.capacity)
    for b in bats:
        if b.capacity != capacities[len(capacities) - 1]:
            print(" pre upgrade", b.id, b.capacity)
            index = capacities.index(b.capacity) + 1
            print("capacity index value", capacities[index])
            b.capacity = capacities[index]
            b.costs = batCosts[index]
            b.maxCapacity = capacities[index]
            upgradeBattery = b
            b.batteryType = index
            break
    print(" post upgrade", upgradeBattery.id, upgradeBattery.capacity)
    district.connectGreedy()
    district.setClosestBattery()
    toBeRemoved = upgradeBattery.closestBattery
    print("remove id", toBeRemoved.id)
    district.batteries.remove(bats[len(bats) - 1])

    print("len ultimate", len(district.batteries))

    for i in range(len(district.batteries)):
        district.batteries[i].id = i

    district.connectGreedy()

    for uc in district.disconnectedHouses:
        hillclimbSwitcher(uc, district, True)

    # #visualize(district)
    if len(district.disconnectedHouses) != 0:
        print("removal failed")
        district.batteries.append(toBeRemoved)
    print("new number of batteries: ", len(district.batteries))

    district = kmeans(district)
    #visualize(district)
    district.compare
    return district