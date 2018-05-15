from functions.manhattan import manhattan

def switch(house, battery):
    # Check if capacity fits output:
    if battery.capacity - house.output >= 0:
        # 1. Update capacity of old battery
        house.connection.capacity += house.output
        # 2. Remove house from list of connected houses in battery object
        house.connection.connectedHouses.remove(house)
        # 3. Change connection
        house.connection = battery
        # 4. Append house to battery list of connected houses
        house.connection.connectedHouses.append(house)
        # 5. Update remaining capacity of new battery
        house.connection.capacity -= house.output
    else:
        print("Not switching house", house.id, "capacity too low")
