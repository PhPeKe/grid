# minimale aantal kleinste batterijen berekenen
# batterijen plaatsen
# greedy + kmeans totdat t niet meer kan
# meest volle batterij upgraden
# etc
from classes.battery import Battery
from algorithms.kmeans import kmeans
from helpers.connectUnconnected import connectUnconnected
from helpers.visualize import visualize
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
        district.batteries.append(battery)
    district.calculateCosts()

    district.connectGreedy()
    district = kmeans(district)

    costDifference = 1
    costDKmeans = 1
    count = 0
    numIt = 10
    while count < numIt:#costDifference > 0:
        oldCosts = copy(district.calculateCosts())
        while costDKmeans > 0:
            print(" while it")
            district = kmeans(district, numIt = 3)
           #visualize(district, True, district.mode + str(x))
            x += 1
            district.calculateCosts()
            costDKmeans = oldCosts - district.costs
        count += 1
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
            break
        #random combinaties maken vak een batterij om te upgraden en een batterij om weg te hale
        # en dan kijken of dat beter wordt
        # nog met simulated annealing
    district.connectGreedy()

    preRemoveCosts = district.calculateCosts()
    toBeRemoved = bats[len(bats)-1]
    district.batteries.remove(bats[len(bats)-1])

    district.connectGreedy()
    for uc in district.disconnectedHouses:
        connectUnconnected(uc, district.batteries)
    district = kmeans(district)

    if len(district.disconnectedHouses) != 0 or preRemoveCosts < district.calculateCosts():
        district.batteries.append(toBeRemoved)

   #visualize(district, True, district.mode + "Ultimate Winner")
    district.compare
    return district

def joinBatteries(district):
    
