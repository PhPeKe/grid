from random import randint, random
from helpers.switch import switch
from helpers.simultaneousSwitch import simultaneousSwitch
from helpers.compare import compare
from helpers.acceptanceProbability import acceptanceprobability


def hillclimbSwitcher(house, district, justUnconnected = False, sa = True, triedhouses = []):
    temperature = 250
    coolingRate = 0.95
    currentCosts = district.calculateCosts()

    if justUnconnected == True:
        if house in district.disconnectedHouses:
            singleConnectUnconnected(house, district)
        return

    else:
        i = 1
        while i < len(district.batteries):
            singleSwitch(house, district, i, triedhouses, currentCosts, sa, temperature, coolingRate)
            i += 1

    combinedSwitch(house, district, 0, 0, temperature, 2, coolingRate)
    return

def singleSwitch(house, district, i, triedhouses, currentCosts, sa, temperature, coolingRate):

    battery = house.possible_connections[i][0]
    capacity_d = house.output

    # sort possible houses to switch with on furthest distance first
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

                    if sa == True:

                        if acceptanceprobability(newCosts, currentCosts, temperature) > random():
                            # # print("NORMAL SWITCH")
                            if house in district.nthChoiceHouses:
                                district.nthChoiceHouses.remove(house)
                            compare(district)
                            temperature *= coolingRate
                            return

                        else:
                            simultaneousSwitch(chosenHouse, house)
                            triedhouses.append(chosenHouse)
                            temperature *= coolingRate

                    if newCosts < currentCosts:
                        if house in district.nthChoiceHouses:
                            district.nthChoiceHouses.remove(house)
                        return
                    else:
                        simultaneousSwitch(chosenHouse, house)
                        triedhouses.append(chosenHouse)


def singleConnectUnconnected(house, district):
    district.batteries.sort(key=lambda x: x.capacity, reverse=True)

    for battery in district.batteries:
        # Find a house which is already connected
        for connectedHouse in battery.connectedHouses:
            oldConnection = connectedHouse.connection
            # then check if the house's output combined with its battery's leftover capacity could facilitate the other
            if (connectedHouse.output + connectedHouse.connection.capacity) > house.output:
                for b in connectedHouse.possible_connections:
                    #print("connect?",b[0].id, b[0].capacity, "connected house cap", connectedHouse.output)
                    if b[0].capacity >= connectedHouse.output:
                        switch(connectedHouse, b[0])
                        switch(house, oldConnection)

                        if house.connection.capacity < 0:
                            house.distance = 0
                            house.connection.capacity += house.output
                            house.connection.connectedHouses.remove(house)
                            house.connection = "NOT CONNECTED!"

                            switch(connectedHouse, oldConnection)
                            break

                        district.disconnectedHouses.remove(house)
                        print("switch! to prev location of: ", connectedHouse.id,"to", oldConnection.id)
                        return
    #print("no possible switches found for house: ", house.id)

#---------------------------------------------------------------------------------------------------------------

def combinedSwitch(house, district, count, bcursor, temperature, howmany, coolingRate):
    currentCosts = district.calculateCosts()
    #geef nummer van batterij mee en increase dat na 100 keer
    # check every battery for randomdistrict.houses to move

    # probeer 10 keer een random combinatie van huizen van dezelfde batterij te vinden
    while howmany < 4:
        while bcursor < len(district.batteries)-1:
            b = district.batteries[bcursor]
            if b != house.connection:
                while count < 10:
                    lookForMultiSwitch(count, b, howmany, house, district, currentCosts, temperature, coolingRate)
                    count += 1
            bcursor += 1
        howmany += 1

    # repeat the previous, but now with larger combination sets, over all batteries
    if howmany < 4:
        howmany += 1
        combinedSwitch(house, district, count, 0, currentCosts, howmany)

    return

def lookForMultiSwitch(count, b, howmany, house, district, currentCosts, temperature, coolingRate):
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

            # move the house
            currentH = house.connection
            switch(house, b)

            for bats in district.batteries:
                if bats.capacity < 0 or b.capacity < 0:
                    multipleSwitchBack(house, currentH, randomh, b, howmany)
                    return

            newCosts = district.calculateCosts()
            if acceptanceprobability(newCosts, currentCosts, temperature) > random():
                if house in district.nthChoiceHouses:
                    district.nthChoiceHouses.remove(house)

                compare(district)
                return
            else:
                multipleSwitchBack(house, currentH, randomh, b, howmany)
            temperature *= coolingRate


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
        switch(house, currentH)

    else:
        house.distance = 0
        house.connection.capacity += house.output
        house.connection.connectedHouses.remove(house)
        house.connection = "NOT CONNECTED!"

    for i in range(howmany):
        # print("PRE COST LOOP", randomh[i].id,"con", randomh[i].connection.id, "to: ", b.id)
        switch(randomh[i], b)
        # print("POST", randomh[i].id,"con", randomh[i].connection.id)

