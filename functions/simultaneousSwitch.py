from functions.manhattan import manhattan


def simultaneousSwitch(house1, house2):
    #if house1.connection.capacity > 0 and house2.connection.capacity > 0:
    # print("SWITCHING: house",house1.id, "with house", house2.id)

    # print("----------Before-----------")
    # print(house1)
    # print(house2,"\n")
    # print(house1.connection)
    # print(house2.connection)

  # 1. Remove house from list of connected houses in battery object
      house1.connection.connectedHouses.remove(house1)
      house2.connection.connectedHouses.remove(house2)

    # 2. "Reset" capacity of batteries
      house1.connection.capacity += house1.output
      house2.connection.capacity += house2.output
    # 3. Change connections
      house1.connection, house2.connection = house2.connection, house1.connection

    # 4. Append house to battery list of connected houses
      house1.connection.connectedHouses.append(house1)
      house2.connection.connectedHouses.append(house2)

     # 5. Recalculate capacity of batteries
      house1.connection.capacity -= house1.output
      house2.connection.capacity -= house2.output

    # 6. Recalculate distance
      house1.distance = manhattan(house1, house1.connection)
      house2.distance = manhattan(house1, house2.connection)

    # print("----------After-----------")
    # print(house1)
    # print(house2,"\n")

    # print(house1.connection)
    # print(house2.connection)

  # else:
  #     print("not switching")

  # if house1.connection.capacity < 0 or house2.connection.capacity < 0:
    #     simultaneousSwitch(house1, house2)