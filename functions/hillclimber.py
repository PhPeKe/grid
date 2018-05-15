from random import randint
from functions.manhattan import manhattan

from functions.calculateCosts import calculateCosts
from functions.switch import switch


def hillclimber(house, district, i, triedhouses, oldcosts):

    currentCosts = calculateCosts(district.houses, district.batteries) # kijken of dit ook in district kan en verschil old en first costs
    battery = house.possible_connections[i][0]
    capacity_d = house.output

    # sort possible houses to switch with on furthest distance first
    # kijken of dit in district zelf kan
    batteryConnections = battery.connectedHouses
    batteryConnections.sort(key=lambda x: x.distance, reverse=True)

    # per battery, see if a switch can be made with one of its houses
    for chosenHouse in batteryConnections:
        if chosenHouse not in triedhouses:

            # Try switching two houses when enough capacity space available
            if ((chosenHouse.output + battery.capacity) >= capacity_d) and (chosenHouse.output < (house.connection.capacity + house.output)):
                switch(house, chosenHouse)
                newCosts = calculateCosts(district.houses, district.batteries)

                if newCosts < currentCosts:
                    print("NORMAL SWITCH")
                    if i == 0:
                        district.nthChoiceHouses.remove(house)
                    return

                else:
                    switch(chosenHouse, house)
                    triedhouses.append(chosenHouse)
    # try each battery
    if 0 <= i < 4:
        hillclimber(house, district, i + 1, triedhouses, oldcosts)

    #combined(house, district, 0, 0, oldcosts, 2)
    return

#---------------------------------------------------------------------------------------------------------------

def combined(house, district, count, bcursor, currentCosts, howmany):
    #geef nummer van batterij mee en increase dat na 100 keer
    count+1

    # check every battery for randomdistrict.houses to move
    # zou nog kunnen met batteryConnections en dan iets sneller
    b = district.batteries[bcursor]

    # probeer 100 keer een random combinatie van huizen van dezelfde batterij te vinden
    if b != house.connection:
        while count < 100:
            count += 1

            randomh = []
            randomid = []
            currentbats = []

            # choose "howmany"-amount of houses randomly from 1 battery,
            bhouses = b.connectedHouses
            c = 0
            while c < howmany:
                #print("c append, c = ", c)
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
                print("SUM", sum, " + B.CAPACITY", b.capacity,"= ", sum + b.capacity, " HOUSE OUTPUT", house.output)
                if (sum + b.capacity >= house.output):

                    currentH = house.connection

                    for i in range(0, howmany):
                        # sla huidige connections op
                        currentbats.append(randomh[i].connection)
                        print("b capacity eerst:", b.capacity)
                        multipleSwitch(randomh[i])

                        if randomh[i].connection.capacity < 0:
                            print("yo hier gaat iets fout")

                    # switch het te verplaatsen huis en update variabelen
                    currentH.capacity += house.output
                    house.connection = b
                    b.capacity -= house.output
                    house.distance = manhattan(house, b)
                    print("B CAPACITY: ", b.capacity, b.id)

                    if b.capacity < 0:
                        print("O KUT")

                    if calculateCosts(district.houses, district.batteries) < currentCosts:
                        print("COMBINED SWITCH")
                        return

                    else:
                        print("combined fail")
                        # terug draaien
                        for i in range(0, howmany):
                            randomh[i].connection = currentbats[i]

                        house.connection = currentH

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

    oldb = randomhouse.connection
    randombatteries = randomhouse.possible_connections

    # check for every battery (starting with smallest distance) whether house could move there
    randombatteries.sort(key=lambda x: x[1])
    for randombattery in randombatteries:
        rb = randombattery[0]

        # if so, moves house there
        if (rb != randomhouse.connection) and (randomhouse.output <= rb.capacity):
                oldb.capacity += randomhouse.output
                print("b capacity na", oldb.capacity, oldb.id)
                randomhouse.connection = rb
                rb.capacity -= randomhouse.output

                randomhouse.distance = manhattan(randomhouse, rb)
    return

 # combinaties optimaliseren
 # één framework voor drie hillclimbers
        # ze naast elkaar leggen en dan de logica naast.
        # dingen zo random mogelijk maken
        # en de minder random dingen als extra funcites te doen
 # comments erbij doen
 # kijken of stoppen  als kabelafstand langer dan de eigen
 # combined is te lang, moet meer als multiple switch, comined moet opgedeeld. Het algoritme kan ook een class worden
 # verplaatsen van batterijen komt er mss bij

 # volgende week dinsdag vroeg mail sturen met wat er allemaal is gedaan
 # repository opschonen!

 # readme moet groter naar template in mailtje met, ook mooi met readme's in folders
 # teveel bestanden hoofdfolder
 # requirements.txt met alle modules die we gebruiken er in zetten
 # randomhillblimber  op andere plek
 # docstrings erbij
 # map functions is nog chaotisch, opdelen in algoritmes en helper functies, kan ook een readme bij die het uitlegt
 #