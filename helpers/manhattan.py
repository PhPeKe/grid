def manhattan(house, battery):
    """manhattan.

    Recieves two objects (usually one house and one battery) that have a
    location attribute and returns the manhattan distance between them.
    """
    return abs(house.location[0] - battery.location[0]) + abs(house.location[1] - battery.location[1])
