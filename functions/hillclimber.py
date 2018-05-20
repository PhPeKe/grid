from random import randint
from functions.switch import switch
from functions.simultaneousSwitch import simultaneousSwitch

def hillclimber(house, district, i, triedhouses):
    currentCosts = district.calculateCosts()  # kijken of dit ook in district kan en verschil old en first costs
    #print("CURRENT COSTS:", currentCosts, "HOUSE: ", house.id)
    if house.connection != "NOT CONNECTED!":
        battery = house.possible_connections[i][0]
        capacity_d = house.output

        # sort possible houses to switch with on furthest distance first
        # kijken of dit in district zelf kan
        # ZOU MEER RANDOM KUNNEN
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
                            #print("NORMAL SWITCH")
                            if i == 0:
                                district.nthChoiceHouses.remove(house)
                            return

                        else:
                            simultaneousSwitch(chosenHouse, house)
                            triedhouses.append(chosenHouse)
        # try each battery
        if 0 <= i < 4:
            #print("new")
            hillclimber(house, district, i + 1, triedhouses)
    else:
        singleConnectUnconnected(house, district)

    combined(house, district, 0, 0, currentCosts, 2)

def singleConnectUnconnected(house, district):
    district.batteries.sort(key=lambda x: x.capacity, reverse=True)
    for battery in district.batteries:
        capacity_d = house.output - battery.capacity
        # Find a house which is already connected
        for connectedHouse in battery.connectedHouses:
            # then check if the house's output combined with its battery's leftover capacity could facilitate the other
            if (connectedHouse.output + connectedHouse.connection.capacity) <= capacity_d:
                for b in connectedHouse.possible_connections:
                        if b[0].capacity >= connectedHouse.output and b != "NOT CONNECTED!":
                            switch(house, b[0])
                            #print("CONNECT UNCONNECTED of house ", house.id)
                            district.disconnectedHouses.remove(house)
                            return

#---------------------------------------------------------------------------------------------------------------

def combined(house, district, count, bcursor, currentCosts, howmany):
    #geef nummer van batterij mee en increase dat na 100 keer
    count+1
    # check every battery for randomdistrict.houses to move
    b = district.batteries[bcursor]

    # probeer 100 keer een random combinatie van huizen van dezelfde batterij te vinden
    if b != house.connection:
        while count < 10:
            count += 1
            if True:
                randomh = []
                randomid = []
                currentbats = []

                # choose "howmany"-amount of houses randomly from 1 battery,
                bhouses = b.connectedHouses
                c = 0
                while c < howmany and len(b.connectedHouses) >= 1:
                    randomh.append(bhouses[randint(0, len(b.connectedHouses)-1)])
                    c += 1

                # check if no doubles in selected houses
                if len(randomh) != len(set(randomh)):
                    # calculate selected houses combined output
                    sum = 0
                    for i in range(howmany):
                        sum = randomh[i].output + sum
                        randomid.append(randomh[i].id)

                    # attempt switch if it would free enough capacity in b
                    if (sum + b.capacity >= house.output):

                        for i in range(0, howmany):
                            # sla huidige connections op
                            currentbats.append(randomh[i].connection)
                            multipleSwitch(randomh[i])

                    if house.connection != "NOT CONNECTED!" and len(currentbats) != 0:
                        currentH = house.connection
                        switch(house, b)

                        for bats in district.batteries:
                            if bats.capacity < 0:
                                multipleSwitchBack(house, currentH, randomh, currentbats, howmany)

                        if district.calculateCosts() < currentCosts:
                            #print("COMBINED SWITCH")
                            return

                        else:
                            multipleSwitchBack(house, currentH, randomh, currentbats, howmany)

    # repeat this process with all the other batteries
    if bcursor < len(district.batteries)-1:
        bcursor += 1
        count = 0
        combined(house, district, count, bcursor, currentCosts, howmany)

    # repeat the previous, but now with larger combination sets, over all batteries
    if howmany < 4:
        howmany += 1
        combined(house, district, count, 0, currentCosts, howmany)

    return

def multipleSwitch(randomhouse):
    randombatteries = randomhouse.possible_connections

    # check for every battery (starting with smallest distance) whether house could move there
    randombatteries.sort(key=lambda x: x[1])
    for randombattery in randombatteries:
        rb = randombattery[0]
        # if so, moves house there
        if rb != randomhouse.connection:
            switch(randomhouse, rb)
            return

def multipleSwitchBack(house, currentH, randomh, currentbats, howmany):
    if house.connection != "NOT CONNECTED!":
        switch(house, currentH)

    else:
        house.distance = 0
        house.connection.capacity += house.output
        house.connection.connectedHouses.remove(house)

    for i in range(0, howmany):
        switch(randomh[i], currentbats[i])


        #nog doen: bug hieruit (iets met update capacity)
        #kleur visualisatie
        #simulated annealing