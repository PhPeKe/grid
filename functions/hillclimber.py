from functions.calculateCosts import calculateCosts
from functions.switch import switch

def hillclimber(house, batteries, houses, i):

    currentCosts = calculateCosts(houses, batteries)
    battery = house.possible_connections[i][0]
    capacity_d = house.output

    # sort possible houses to switch with on furthest distance first
    batteryConnections = battery.connectedHouses
    batteryConnections.sort(key=lambda x: x.distance, reverse=True)

    for cHouse in batteryConnections:
        # Try switching two houses when enough capacity space available
        if (cHouse.output + battery.capacity) >= capacity_d:
            print("house: ", house.id)
            switch(house, cHouse)
            newCosts = calculateCosts(houses, batteries)

            if newCosts < currentCosts:
                return

            else:
                switch(house, cHouse)
                # repeat until the costs are lower, or until all batterieconnections have been tried
                if 0 <= i < 4:
                    hillclimber(house, batteries, houses, i+1)
            return
