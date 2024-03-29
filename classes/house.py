from helpers.manhattan import manhattan
from random import shuffle

class House:
    """House.

    Class House:
    - Holds all necessary information about a house
    - Has methods to connect the house to a battery: greedy or random
    """
    def __init__(self, x, y, output, id):
        self.location = (x,y)
        self.output = output
        self.id = id
        self.distance = 1000
        self.connection = set()
        self.possible_connections = []

    # Greedy algorithm that connects houses to nearest battery
    def connectNearestBattery(self, batteries, district):
        """connectNearestBattery.

        Connects a house to the nearest battery if possible if it fits in the
        capacity.
        """
        for battery in batteries:
            distance = manhattan(self, battery)
            # Save all possible connections
            possible_connection = (battery, distance)
            self.possible_connections.append(possible_connection)

                # Check if distance of this battery is closer than last
            if distance < self.distance and battery.capacity > self.output:
                # Safe distance in House object
                self.distance = distance
                # Connect to battery
                self.connection = battery

        if self.connection != possible_connection[0]:
            district.nthChoiceHouses.append(self)

        # Catch error if no connection could be made
        if self.connection == "NOT CONNECTED!":
            district.disconnectedHouses.append(self)
            district.allConnected = False

        elif not self.connection == set():
            #print("connection: ", self.connection)
            if type(self.connection) is str:
                print("!!",self.id, self.connection)
            self.connection.capacity -= self.output
            # Append reference to houses connected to battery
            self.connection.connectedHouses.append(self)
        else:
            #print("Error: House", str(self.id), "COULD NOT BE CONNECTED!")
            self.connection = "NOT CONNECTED!"
            district.disconnectedHouses.append(self)
            district.allConnected = False


    def connectRandomBattery(self, batteries, district):
        shuffle(batteries)
        for battery in batteries:
            distance = manhattan(self, battery)
            # Save all possible connections
            possible_connection = (battery, distance)
            self.possible_connections.append(possible_connection)

            # Connect if capacity is enough
            if battery.capacity > self.output:
                # Safe distance in House object
                self.distance = distance
                # Connect to battery
                self.connection = battery

        # Sort back to fix plotting bug
        batteries.sort(key = lambda x: x.id)

        if self.connection != possible_connection[0]:
            district.nthChoiceHouses.append(self)

        # Catch error if no connection could be made
        if not self.connection == set():
            self.connection.capacity -= self.output
            # Append reference to houses connected to battery
            self.connection.connectedHouses.append(self)
        else:
            print("Error: House",str(self.id),"COULD NOT BE CONNECTED!")
            self.connection = "NOT CONNECTED!"
            district.disconnectedHouses.append(self) # even in district zelf laten maken.
            district.allConnected = False

        # Sort list with possible connections
        self.possible_connections.sort(key = lambda x: x[1])

    # Makes houses printable
    def __str__(self):
        """Comment like this"""
        if self.connection == set() or self.connection == "NOT CONNECTED!":
            return ("House " + str(self.id) + " at " + str(self.location) + " has an output of " + str(self.output))
        else:
            return ("House " + str(self.id) + " at " + str(self.location) + " has an output of " + str(self.output) + " and is connected to Battery " + str(self.connection.id) + " which is " + str(self.distance) + " meters away at " + str(self.connection.location))
