from functions.calculateCosts import calculateCosts
from functions.switch import switch

def hillclimber(nthChoiceHouse, batteries, houses, i):

    currentCosts = calculateCosts(houses, batteries)
    battery = nthChoiceHouse.possible_connections[i][0]
    capacity_d = nthChoiceHouse.output - battery.capacity

    batteryConnections = battery.connectedHouses
    batteryConnections.sort(key=lambda x: x.distance, reverse=True)

    for cHouse in batteryConnections:

        if (cHouse.output + battery.capacity) >= capacity_d:
            print("nthChoiceHouse: ", nthChoiceHouse)
            switch(nthChoiceHouse, cHouse)
            newCosts = calculateCosts(houses, batteries)

            if newCosts < currentCosts:
                return

            else:
                switch(nthChoiceHouse, cHouse)
                if 1 <= i < 4:
                    hillclimber(nthChoiceHouse, batteries, houses, i+1)
            return
