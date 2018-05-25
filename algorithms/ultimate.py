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
    temperature = 500
    coolingRate = 0.95
    count = 0
    numIt = 10
    while temperature > 1:
        print("temperature: ",temperature)
        oldCosts = copy(district.calculateCosts())
        while costDKmeans > 0:
            print("new kmeans iteration")
            oldCosts = copy(district.calculateCosts())
            district = kmeans(district, numIt = 10)
            x += 1
            district.calculateCosts()
            costDKmeans = oldCosts - district.costs
        count += 1
        district = joinClosestBatteries(district, batCosts)
        if acceptanceprobability(district.calculateCosts(), oldCosts, temperature) < random():
            break
        temperature *= coolingRate
        costDKmeans = 1
    district = kmeans(district)
    district.calculateCosts()
    print("post ultimate costs:", district.costs)
    return district

def joinClosestBatteries(district, batCosts):
    district.setClosestBattery()
    district.batteries.sort(key = lambda x: x.closestBatteryDistance)
    closestBatteries = [district.batteries[0], district.batteries[0].closestBattery]

    if closestBatteries[0].batteryType != 2 and closestBatteries[1].batteryType != 2:
        usedCapacity0 = closestBatteries[0].maxCapacity - closestBatteries[0].capacity
        usedCapacity1 = closestBatteries[1].maxCapacity - closestBatteries[1].capacity
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

            # Update Battery-id's
            for i in range(len(district.batteries)):
                district.batteries[i].id = i

            kmeans(district, numIt=1)
    return district
