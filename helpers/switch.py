from helpers.manhattan import manhattan

def switch(house, battery):
    # 1. Update capacity of old battery
    if house.connection != "NOT CONNECTED!":
        house.connection.capacity += house.output
    # 2. Remove house from list of connected houses in battery object
        house.connection.connectedHouses.remove(house)
    # 3. Change connection
    house.connection = battery
    # 4. Append house to battery list of connected houses
    house.connection.connectedHouses.append(house)
    # 5. Update remaining capacity of new battery
    house.connection.capacity -= house.output
    # 6. Recalculate distance
    house.distance = manhattan(house, house.connection)
