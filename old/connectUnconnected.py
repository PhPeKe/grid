def connectUnconnected(house, batteries):

    batteries.sort(key=lambda x: x.capacity, reverse=True)
    for battery in batteries:
        capacity_d = house.output - battery.capacity

        # Find a house which is already connected
        for connectedHouse in battery.connectedHouses:
            # then check if the house's output combined with its battery's leftover capacity could facilitate the other
            if (connectedHouse.output + connectedHouse.connection.capacity) <= capacity_d:

                for b in connectedHouse.possible_connections:
                    if b[0].capacity >= connectedHouse.output:
                        oldconnection = connectedHouse.connection
                        connectedHouse.connection = b[0]
                        house.connection = oldconnection
                        print("SWITCH of house ", house.id, " and house ", connectedHouse.id)
                        return

    print("no possible switches found for house: ", house)
