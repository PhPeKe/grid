def manhattan(house, battery):
    """Calculates manhatten distance between a house and its connected battery"""
    return abs(house.location[0] - battery.location[0]) + \
           abs(house.location[1] - battery.location[1])
