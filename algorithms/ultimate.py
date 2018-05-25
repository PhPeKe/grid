from classes.battery import Battery
from algorithms.kmeans import kmeans
from helpers.acceptanceProbability import acceptanceprobability
from random import random
from copy import copy


def ultimate(district):
    """Optimizes the district's costs with placing different types of batteries

       Keyword arguments:
       batcosts - the costs of a battery with increasing capacity
       costDKmean - keeps track of the cost difference with the previous iteration of kmeans

       Flow:
    1. Places the minimum possible amount of lowest-capacity batteries
    2. Optimizes the battery placement with kmeans
    3. Combines two nearby batteries into one with a higher capacity until the temperature "cools" down
    4. To prevent local minima with simulated annealing, slightly more expensive configurations
               are accepted too
    5. The district is set to the overall cheapest configuration

    """
    print("ULTIMATE")
    district.mode = "ultimate-"
    x = 0
    batCosts = [900, 1350, 1800]
    totalOutput = 0
    for house in district.houses:
        totalOutput = totalOutput + house.output

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

    costDKmeans = 1
    temperature = 500
    coolingRate = 0.95
    count = 0

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
    """ joins two nearby batteries into one larger battery

       Keyword arguments:
       usedCapacity = how much of a battery's capacity is used

       Flow:
    1. Selects the two batteries which are closest together
    2. Upgrades the first battery
    3. Connects the 2nd battery's houses to the other and updates
    4. Locates joined battery to the center of its houses

    """

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
