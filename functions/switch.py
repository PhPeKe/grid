from functions.manhattan import manhattan

def switch(house1, house2):

    #print("SWITCHING: house",house1.id, "with house", house2.id)

    #print("----------Before-----------")
    #print(house1)
    #print(house2,"\n")

    #print(house1.connection)
    #print(house2.connection)

    # 1. "Reset" capacity of batteries
    house1.connection.capacity += house1.output
    house2.connection.capacity += house2.output

    # 2. Change connections
    house1.connection, house2.connection = house2.connection, house1.connection

    # 3. Recalculate capacity of batteries
    house1.connection.capacity -= house1.output
    house2.connection.capacity -= house2.output

    # 4. Recalculate distance
    house1.distance = manhattan(house1, house1.connection)
    house2.distance = manhattan(house1, house2.connection)

    #print("----------After-----------")
    #print(house1)
    #print(house2,"\n")

    #print(house1.connection)
    #print(house2.connection)

    if house1.connection.capacity < 0 or house2.connection.capacity < 0:
        switch(house1,house2)
