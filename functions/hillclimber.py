from random import randint
from functions import visualize
from functions.switch import switch
from functions.simultaneousSwitch import simultaneousSwitch
from copy import deepcopy
from math import exp

def hillclimbSwitcher(house, district, i, triedhouses):
    temperature = 250

    currentCosts = district.calculateCosts()  # kijken of dit ook in district kan en verschil old en first costs

    if house.connection != "NOT CONNECTED!":
        while i < len(district.batteries):
            # print("CURRENT COSTS:", currentCosts, "HOUSE: ", house.id)

            battery = house.possible_connections[i][0]
            capacity_d = house.output

            # sort possible houses to switch with on furthest distance first
            # kijken of dit in district zelf kan
            batteryConnections = battery.connectedHouses
            batteryConnections.sort(key=lambda x: x.distance, reverse=True)

            # per battery, see if a switch can be made with one of its houses
            for chosenHouse in batteryConnections:
                if chosenHouse not in triedhouses and chosenHouse != house:

                    # Try switching two houses when enough capacity space available
                    if ((chosenHouse.output + battery.capacity) >= capacity_d) and \
                            (chosenHouse.output < (house.connection.capacity + house.output)):
                        simultaneousSwitch(house, chosenHouse)

                        if house.connection.capacity < 0 or chosenHouse.connection.capacity < 0:
                            simultaneousSwitch(chosenHouse, house)
                            triedhouses.append(chosenHouse)

                        else:
                            newCosts = district.calculateCosts()

                            if newCosts < currentCosts:
                                # # print("NORMAL SWITCH")
                                if house in district.nthChoiceHouses:
                                    district.nthChoiceHouses.remove(house)

                                if district.costs < district.compare.costs and len(district.disconnectedHouses) == 0:
                                    district.compare = deepcopy(district)
                                return
                            elif newCosts < currentCosts + temperature:
                                if house in district.nthChoiceHouses:
                                    district.nthChoiceHouses.remove(house)
                                temperature * 0.95
                                # print("normal annealing")

                                return

                            else:
                                simultaneousSwitch(chosenHouse, house)
                                triedhouses.append(chosenHouse)
            i += 1

    else:
        singleConnectUnconnected(house, district)

    combined(house, district, 0, 0, temperature, 2)
    return


def singleConnectUnconnected(house, district):
    district.batteries.sort(key=lambda x: x.capacity, reverse=True)
    for battery in district.batteries:
        capacity_d = house.output - battery.capacity
        # Find a house which is already connected
        for connectedHouse in battery.connectedHouses:
            # then check if the house's output combined with its battery's leftover capacity could facilitate the other
            if (connectedHouse.output + connectedHouse.connection.capacity) <= capacity_d:

                for b in connectedHouse.possible_connections:
                    # # print(b)
                    if b[0].capacity >= connectedHouse.output and b != "NOT CONNECTED!":
                        # # print(house.connection)
                        switch(house, b[0])

                        if house.connection.capacity < 0:
                            # # print("yo")
                            house.distance = 0
                            house.connection.capacity += house.output
                            # # # print(house.id)
                            house.connection.connectedHouses.remove(house)
                            house.connection = "NOT CONNECTED!"
                            break

                        # # print("CONNECT UNCONNECTED of house ", house.id, "to", house.connection.id, house.connection.capacity)
                        district.disconnectedHouses.remove(house)
                        return

#---------------------------------------------------------------------------------------------------------------

def combined(house, district, count, bcursor, temperature, howmany):
    currentCosts = district.calculateCosts()
    #geef nummer van batterij mee en increase dat na 100 keer
    # check every battery for randomdistrict.houses to move

    # probeer 10 keer een random combinatie van huizen van dezelfde batterij te vinden
    while howmany < 4:
        while bcursor < len(district.batteries)-1:
            b = district.batteries[bcursor]
            if b != house.connection:
                while count < 10:
                    lookForMultiSwitch(count, b, howmany, house, district, currentCosts, temperature)
                    count += 1
            bcursor += 1
        howmany += 1

    # repeat the previous, but now with larger combination sets, over all batteries
    if howmany < 4:
        howmany += 1
        combined(house, district, count, 0, currentCosts, howmany)

    return

def lookForMultiSwitch(count, b, howmany, house, district, currentCosts, temperature):
    randomh = []
    # choose "howmany"-amount of houses randomly from 1 battery,
    bhouses = b.connectedHouses
    c = 0
    while c < howmany and len(b.connectedHouses) >= 1:
        randomh.append(bhouses[randint(0, len(b.connectedHouses) - 1)])
        c += 1

    # check if no doubles in selected houses
    if len(randomh) == len(set(randomh)):
        # calculate selected houses combined output
        sum = 0
        for i in range(howmany):
            sum = randomh[i].output + sum

        # attempt switch if it would free enough capacity in b
        if (sum + b.capacity >= house.output):

            for i in range(howmany):
                # save current connection
                multipleSwitch(randomh[i])
                #if randomh[i].connection == b:
                    #return

            # print("found different bats?")
            # move the house
            currentH = house.connection
            switch(house, b)

            for bats in district.batteries:
                if bats.capacity < 0 or b.capacity < 0:
                    multipleSwitchBack(house, currentH, randomh, b, howmany)
                    return

            newcosts = district.calculateCosts()
            if newcosts < currentCosts:
                # print("new", newcosts, "current", currentCosts)
                # print(house.id, randomh[0].id, randomh[1].id)
                #print("COMBINED SWITCH, house:", house.id, house.connection.id, "combi1", randomh[0].id,
                      #randomh[0].connection.id)
                return
            elif newcosts < currentCosts + temperature:
                # print("combined annealing")
                temperature = temperature * 0.95
                return
            else:
                # print("PRE COST LOOP", "new", newcosts, "current", currentCosts)
                multipleSwitchBack(house, currentH, randomh, b, howmany)
                # print("POST", "new", district.calculateCosts(), "current", currentCosts)


def multipleSwitch(randomhouse):
    randombatteries = randomhouse.possible_connections
    # check for every battery (starting with smallest distance) whether house could move there
    randombatteries.sort(key=lambda x: x[1])
    currentbattery = randomhouse.connection
    for randombattery in randombatteries:
        rb = randombattery[0]
        if rb != currentbattery:
            if rb.capacity >= randomhouse.output:
                # print("batteries", rb.id, randomhouse.connection.id)
                switch(randomhouse, rb)
                return

def multipleSwitchBack(house, currentH, randomh, b, howmany):
    if currentH != "NOT CONNECTED!":
        # print("HOUSE pre switch back: ", house.id, "con", house.connection.id, "currentH: ", currentH)
        switch(house, currentH)
        # print("HOuSE post: ", house.id, "con", house.connection.id)

    else:
        house.distance = 0
        house.connection.capacity += house.output
        house.connection.connectedHouses.remove(house)
        house.connection = "NOT CONNECTED!"

    for i in range(howmany):
        # print("PRE COST LOOP", randomh[i].id,"con", randomh[i].connection.id, "to: ", b.id)
        switch(randomh[i], b)
        # print("POST", randomh[i].id,"con", randomh[i].connection.id)

def acceptanceprobability(newCosts, currentCosts, temperature):
    if newCosts < currentCosts:
        return 1.0
    else:
        return exp((currentCosts - newCosts) / temperature)
