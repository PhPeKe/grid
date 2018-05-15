from random import randint
from functions.manhattan import manhattan
from functions.switch import switch
from functions.simultaneousSwitch import simultaneousSwitch


def hillclimber(house, district, i, triedhouses):

    currentCosts = district.calculateCosts() # kijken of dit ook in district kan en verschil old en first costs

    print("CURRENT COSTS:", currentCosts, "HOUSE: ", house.id)
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
            if ((chosenHouse.output + battery.capacity) >= capacity_d) and (chosenHouse.output < (house.connection.capacity + house.output)):
                simultaneousSwitch(house, chosenHouse)

                if house.connection.capacity < 0 or chosenHouse.connection.capacity < 0:
                    simultaneousSwitch(chosenHouse, house)
                    triedhouses.append(chosenHouse)

                else:

                    newCosts = district.calculateCosts()

                    if newCosts < currentCosts:
                        print("NORMAL SWITCH")
                        if i == 0:
                            district.nthChoiceHouses.remove(house)
                        return

                    else:
                        simultaneousSwitch(chosenHouse, house)
                        triedhouses.append(chosenHouse)
    # try each battery
    if 0 <= i < 4:
        hillclimber(house, district, i + 1, triedhouses)

    combined(house, district, 0, 0, currentCosts, 2)

#---------------------------------------------------------------------------------------------------------------

def combined(house, district, count, bcursor, currentCosts, howmany):
    #geef nummer van batterij mee en increase dat na 100 keer
    count+1
    print("combined aangeroepen")
    currentH = house.connection

    # check every battery for randomdistrict.houses to move
    # zou nog kunnen met batteryConnections en dan iets sneller
    b = district.batteries[bcursor]

    # probeer 100 keer een random combinatie van huizen van dezelfde batterij te vinden
    if b != house.connection:
        #print("new 100")
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
                    if (sum + b.capacity >= house.output):

                        for i in range(0, howmany):
                            # sla huidige connections op
                            currentbats.append(randomh[i].connection)
                            multipleSwitch(randomh[i])

                        #print("SWITCH MAIN PRE:",house, house.connection.id)
                        #print("CURRENTH: ", currentH.id, "B: ", b.id)
                        switch(house, b)
                        #print("SWITCH MAIN POST:",house, house.connection.id)

                        for bats in district.batteries:
                            if bats.capacity < 0:
                                #print("fout")

                                # print("SWITCH BACK MAIN POST:",bats.id, bats.capacity)
                                switch(house, currentH)
                                # print("SWITCH BACK MAIN POST:",bats.id, bats.capacity)

                                # terug draaien
                                for i in range(0, howmany):
                                    # print("SWITCH BACK RANDOM PRE:",randomh[i], randomh[i].connection.id)
                                    switch(randomh[i], currentbats[i])
                                    # print("SWITCH BACK RANDOM POST:",randomh[i], randomh[i].connection.id)


                        if district.calculateCosts() < currentCosts:
                            #print("COMBINED SWITCH")
                            return

                        else:
                            #print("SWITCH BACK MAIN PRE:",house, house.connection.id)

                            switch(house, currentH)
                            #print("SWITCH BACK MAIN POST:",house, house.connection.id)
                            #print(currentbats)

                            # terug draaien
                            for i in range(0, howmany):
                                #print("SWITCH BACK RANDOM PRE:",randomh[i], randomh[i].connection.id)
                                #print(currentbats[i].id)
                                switch(randomh[i], currentbats[i])
                                #print("SWITCH BACK RANDOM POST:",randomh[i], randomh[i].connection.id)


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
