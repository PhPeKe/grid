def switch(house1, house2):

    # Save temp
    temp = house1

    # 1. "Reset" capacity of batteries
    house1.connection.capacity += house1.output
    house2.connection.capacity += house2.output

    # 2. Change connections
    house1.connection = house2.connection
    house2.connection = temp.connection

    # 3. Recalculate capacity of batteries
    house1.connection.capacity -= house1.output
    house2.connection.capacity -= house2.output

    if house1.connection.capacity < 0 or house2.connection.capacity < 0:
        print("ERROR: switching is illegal")
        return False
    
    return True
