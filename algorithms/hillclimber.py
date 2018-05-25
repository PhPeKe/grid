from random import randint, random
from helpers.switch import switch
from helpers.simultaneousSwitch import simultaneousSwitch
from helpers.compare import compare
from helpers.acceptanceProbability import acceptanceprobability


def hillclimbSwitcher(house, district, justUnconnected = False, justSingle = False, sa = True,\
                      temperature = 250, coolingRate = 0.95 ):
    """ Iterates towards a connection for every house and a cheaper cable configuration

       Keyword arguments:
       house - House object for which the method searches an alternative cable connection
       district - current district in which the houses, batteries and cables exist
       """
    
    if justUnconnected:
        if house in district.disconnectedHouses:
            singleConnectUnconnected(house, district)
        return

    else:
        i = 1
        triedHouses = []
        currentCosts = district.calculateCosts()
        while i < len(district.batteries):
            singleSwitch(house, district, i, triedHouses, currentCosts, sa, temperature, coolingRate)
            i += 1

    if not justSingle:
        combinedSwitch(house, district, 0, 0, temperature, 2, coolingRate, sa)

    return


def singleSwitch(house, district, i, triedHouses, currentCosts, sa, temperature, coolingRate):
    """Optimizes cable configuration by switching 2 houses.

       Keyword arguments:
       chosenHouse - House object that's being considered for a switch with house
       triedHouses - houses which have already been considered
       """

    battery = house.possible_connections[i][0]

    # first attempts to switch with houses who are far from their battery
    # considers every house of every battery until a switch is found
    batteryConnections = battery.connectedHouses
    batteryConnections.sort(key=lambda x: x.distance, reverse=True)

    for chosenHouse in batteryConnections:
        if chosenHouse not in triedHouses and chosenHouse != house:
            if ((chosenHouse.output + battery.capacity) >= house.output) and \
                    (chosenHouse.output < (house.connection.capacity + house.output)):
                simultaneousSwitch(house, chosenHouse)

                if house.connection.capacity < 0 or chosenHouse.connection.capacity < 0:
                    simultaneousSwitch(chosenHouse, house)
                    triedHouses.append(chosenHouse)

                else:
                    newCosts = district.calculateCosts()

                    # simulated annealing
                    if sa:
                        if acceptanceprobability(newCosts, currentCosts, temperature) > random():
                            if house in district.nthChoiceHouses:
                                district.nthChoiceHouses.remove(house)

                            compare(district)
                            temperature *= coolingRate
                            return

                        else:
                            simultaneousSwitch(chosenHouse, house)
                            triedHouses.append(chosenHouse)
                            temperature *= coolingRate

                    if newCosts < currentCosts:
                        if house in district.nthChoiceHouses:
                            district.nthChoiceHouses.remove(house)
                        return
                    else:
                        simultaneousSwitch(chosenHouse, house)
                        triedHouses.append(chosenHouse)


def singleConnectUnconnected(house, district):
    """Finds a connection for an unconnected house,

       Keyword arguments:
       house - the House object without which must be connected
       connectedHouse - House object that's being considered to make space for 'house'
       """
    district.batteries.sort(key=lambda x: x.capacity, reverse=True)

    for battery in district.batteries:
        # Finds a house which can move elsewhere, the unconnected house takes its place
        for connectedHouse in battery.connectedHouses:
            oldConnection = connectedHouse.connection

            if (connectedHouse.output + connectedHouse.connection.capacity) > house.output:
                for b in connectedHouse.possible_connections:
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


def combinedSwitch(house, district, count, bCursor, temperature, howMany, coolingRate, sa, combiSize = 4):
    """Optimizes cable configuration by replacing multiple houses, another house takes their place

       Keyword arguments:
       combiSize - determines how large the group of houses will be to make the combined switch
       howMany - keeps track of how large the group of houses currently is
       connectedHouse - House object that's being considered to make space for 'house'

       """
    currentCosts = district.calculateCosts()

    # probeer 10 keer een random combinatie van huizen van dezelfde batterij te vinden
    while howMany < combiSize:
        while bCursor < len(district.batteries)-1:
            b = district.batteries[bCursor]
            if b != house.connection:
                while count < 10:
                    lookForMultiSwitch(sa, b, howMany, house, district, currentCosts, temperature, coolingRate)
                    count += 1
            bCursor += 1
        howMany += 1

    # repeat the previous, but now with larger combination sets, over all batteries
    if howMany < 4:
        howMany += 1
        combinedSwitch(house, district, count, 0, currentCosts, howMany)

    return


def lookForMultiSwitch(sa, b, howMany, house, district, currentCosts, temperature, coolingRate):
    randomH = []
    # choose "howMany"-amount of houses randomly from 1 battery,
    bhouses = b.connectedHouses
    c = 0
    while c < howMany and len(b.connectedHouses) >= 1:
        randomH.append(bhouses[randint(0, len(b.connectedHouses) - 1)])
        c += 1

    # check if no doubles in selected houses
    if len(randomH) == len(set(randomH)):
        # calculate selected houses combined output
        sum = 0
        for i in range(howMany):
            sum = randomH[i].output + sum

        # attempt switch if it would free enough capacity in b
        if (sum + b.capacity >= house.output):
            for i in range(howMany):
                # save current connection
                multipleSwitch(randomH[i])

            # move the house
            currentH = house.connection
            switch(house, b)

            for bats in district.batteries:
                if bats.capacity < 0 or b.capacity < 0:
                    multipleSwitchBack(house, currentH, randomH, b, howMany)
                    return

            newCosts = district.calculateCosts()
            if sa:
                if acceptanceprobability(newCosts, currentCosts, temperature) > random():
                    if house in district.nthChoiceHouses:
                        district.nthChoiceHouses.remove(house)
                    compare(district)
                    return
                else:
                    multipleSwitchBack(house, currentH, randomH, b, howMany)
                temperature *= coolingRate
            else:
                if newCosts < currentCosts:
                    if house in district.nthChoiceHouses:
                        district.nthChoiceHouses.remove(house)
                    return
                else:
                    multipleSwitchBack(house, currentH, randomH, b , howMany)



def multipleSwitch(randomhouse):
    randombatteries = randomhouse.possible_connections

    # check for every battery (starting with smallest distance) whether house could move there
    randombatteries.sort(key=lambda x: x[1])
    currentbattery = randomhouse.connection
    for randombattery in randombatteries:
        rb = randombattery[0]
        if rb != currentbattery:
            if rb.capacity >= randomhouse.output:
                switch(randomhouse, rb)
                return


def multipleSwitchBack(house, currentH, randomH, b, howMany):
    if currentH != "NOT CONNECTED!":
        switch(house, currentH)

    else:
        house.distance = 0
        house.connection.capacity += house.output
        house.connection.connectedHouses.remove(house)
        house.connection = "NOT CONNECTED!"

    for i in range(howMany):
        switch(randomH[i], b)
