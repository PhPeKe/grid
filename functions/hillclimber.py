from random import randint

from functions.calculateCosts import calculateCosts
from functions.switch import switch


def hillclimber(house, district, i, triedhouses, oldcosts):

    currentCosts = calculateCosts(district.houses, district.batteries)
    battery = house.possible_connections[i][0]
    capacity_d = house.output

    # sort possible houses to switch with on furthest distance first
    batteryConnections = battery.connectedHouses
    batteryConnections.sort(key=lambda x: x.distance, reverse=True)

    for cHouse in batteryConnections:
        if cHouse not in triedhouses:
            # Try switching two houses when enough capacity space available
            if ((cHouse.output + battery.capacity) >= capacity_d) and (cHouse.output < (house.connection.capacity + house.output)):

                switch(house, cHouse)
                newCosts = calculateCosts(district.houses, district.batteries)

                if newCosts < currentCosts:
                    print("NORMAL SWITCH")
                    if i == 0:
                        district.nthChoiceHouses.remove(house)
                    return

                elif newCosts == currentCosts:
                    triedhouses.append(cHouse)

                else:
                    switch(cHouse, house)
                    triedhouses.append(cHouse)

    if 0 <= i < 4:
        hillclimber(house, district, i + 1, triedhouses, oldcosts)

    combined(house, district, 0, 0, oldcosts, 2)
    return


def combined(house, district, count, bcursor, currentCosts, howmany):
    #geef nummer van batterij mee en increase dat na 100 keer
    count+1

    # check every battery for randomdistrict.houses to move
    b = district.batteries[bcursor]

    # probeer 100 keer een random combinatie van huizen van dezelfde batterij te vinden
    while count < 100:
        count += 1
        randomh = []
        randomid = []
        currentbats = []
        if house.connection != b:
            # choose 2district.houses randomly from 1 battery
            bhouses = b.connectedHouses

            c = 0
            while c < howmany:
                #print("c append, c = ", c)
                randomh.append(bhouses[randint(0, len(b.connectedHouses)-1)])
                c += 1

            sum = 0
            for i in range(howmany):
                sum = randomh[i].output + sum
                randomid.append(randomh[i].id)
            #print("houses", randomid)

            # randomhouse = bhouses[randint(0, len(b.connectedHouses)-1)]
            # randomhouse2 = bhouses[randint(0, len(b.connectedHouses)-1)]
#len(your_list) != len(set(your_list))
            # when these 2 aren't the same house and would make enough free space, switch

            if len(randomh) != len(set(randomh)):
                #print("not same length")
                #print("check sum: ", sum, " vrije ruimte batt: ", house.connection.capacity, "<= output", house.output)
                if (sum + b.capacity >= house.output):

                    #print("sum check, sum = ", sum)
                    currentH = house.connection

                    for i in range(0, howmany):

                        #print("switch multiple")
                        currentbats.append(randomh[i].connection)
                        multipleSwitch(randomh[i])

                    if b.capacity < 0:
                        print("O KUT")

                    house.connection = b
                    b.capacity -= house.output
                    currentH.capacity += house.output

                    if calculateCosts(district.houses, district.batteries) < currentCosts:
                        print("COMBINED SWITCH")
                        return

                    else:
                        print("combined fail")
                        # terug draaien
                        for i in range(0, howmany):
                            randomh[i].connection = currentbats[i]

                        house.connection = currentH

    if bcursor < len(district.batteries)-1:
        bcursor += 1
        count = 0
        combined(house, district, count, bcursor, currentCosts, howmany)

    if howmany < 4:
        howmany += 1
        combined(house, district, count, 0, currentCosts, howmany)

    return

def multipleSwitch(randomhouse):

    oldb = randomhouse.connection
    randombatteries = randomhouse.possible_connections
    randombatteries.sort(key=lambda x: x[1])
    for randombattery in randombatteries:
        rb = randombattery[0]

        if (rb != randomhouse.connection) and (randomhouse.output <= rb.capacity):
            if(rb.capacity - randomhouse.output >= 0):
                randomhouse.connection = rb
                rb.capacity -= randomhouse.output
                oldb.capacity += randomhouse.output
    return





 # combinaties optimaliseren

 # één framework voor drie hillclimbers
 # kan de variabele eruit voor district.batteries[]?
 # comments erbij doen
    # kijken of stoppen  als kabelafstand langer dan de eigen