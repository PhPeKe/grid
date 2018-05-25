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
       
       Flow:
    1. A 'chosenHouse' is selected from the house its possible connections, nearby batteries first
    2. Check whether a switch with this house is possible and decreases the costs 
       (can be with or without simulated annealing)
    3. If the houses don't switch, continue to the next house, possibly at the next battery
    
    """

    battery = house.possible_connections[i][0]

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
       
       Flow:
    1. Selects a house to move elsewhere, starting at the batteries nearest to 'house'
    2. If the house can, it moves elsewhere, 
    3. The unconnected house takes its place
    
    """
    district.batteries.sort(key=lambda x: x.capacity, reverse=True)

    for battery in district.batteries:
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
       connectedHouse - House object that's being considered to make space for 'house'
       combiSize - determines how large the group of houses will be to make the combined switch
       howMany - keeps track of how large the group of houses currently is
       bCursor - keeps track of which battery is being considered for 
       count - determines number of iterations for looking for a possible group of houses to switch
        
        Flow:
        1. Selects a number of 'howMany' houses, all connected to one battery, to move elsewhere,
        2. If no switch is made, continue trying for 'count' amount of times
        3. If no switch is made, continue to the next battery     
        4. If no switch is made, increase the size of the group of houses
    """
    currentCosts = district.calculateCosts()

    # probeer 10 keer een random combinatie van huizen van dezelfde batterij te vinden
    while howMany < combiSize:
        while bCursor < len(district.batteries)-1:
            b = district.batteries[bCursor]
            if b != house.connection:
                while count < 10:
                    lookForMultiSwitch(sa, b, howMany, house, district, currentCosts, \
                                       temperature, coolingRate)
                    count += 1
            bCursor += 1
        howMany += 1

    if howMany < 4:
        howMany += 1
        combinedSwitch(house, district, count, 0, currentCosts, howMany)



def lookForMultiSwitch(sa, b, howMany, house, district, currentCosts, temperature, coolingRate):
    """Searches for a group of houses that could do a combined switch

       Keyword arguments:
       randomH - list with the houses in the switch group

       Flow:
    1. Chooses random houses from the ones that are connected to a battery
    2. Check whether a switch with these houses is possible and decreases the costs 
       (can be with or without simulated annealing)
       
    """
    randomH = []
    # choose "howMany"-amount of houses randomly from 1 battery,
    bhouses = b.connectedHouses
    c = 0
    while c < howMany and len(b.connectedHouses) >= 1:
        randomH.append(bhouses[randint(0, len(b.connectedHouses) - 1)])
        c += 1
    
    # check if there are no doubles in the group
    if len(randomH) == len(set(randomH)):
        sum = 0
        for i in range(howMany):
            sum = randomH[i].output + sum

        if (sum + b.capacity >= house.output):
            for i in range(howMany):
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
    """ Moves a group of houses to different batteries """
    
    randomBatteries = randomhouse.possible_connections

    randomBatteries.sort(key=lambda x: x[1])
    currentbattery = randomhouse.connection
    for randomBattery in randomBatteries:
        rb = randomBattery[0]
        if rb != currentbattery:
            if rb.capacity >= randomhouse.output:
                switch(randomhouse, rb)
                return


def multipleSwitchBack(house, currentH, randomH, b, howMany):
    """ Moves a group of houses back to their previous battery """

    if currentH != "NOT CONNECTED!":
        switch(house, currentH)

    else:
        house.distance = 0
        house.connection.capacity += house.output
        house.connection.connectedHouses.remove(house)
        house.connection = "NOT CONNECTED!"

    for i in range(howMany):
        switch(randomH[i], b)
