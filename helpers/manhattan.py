def manhattan(house, battery):
    return abs(house.location[0] - battery.location[0]) + abs(house.location[1] - battery.location[1])
