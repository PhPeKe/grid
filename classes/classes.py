from functions.manhattan import manhattan
from functions.calculateCosts import calculateCosts
import csv
from random import shuffle

class House:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.output = output
        self.id = id
        self.distance = 1000
        self.connection = set()
        self.possible_connections = []

    # Greedy algorithm that connects houses to nearest battery
    def connectNearestBattery(self, batteries):
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

    def connectRandomBattery(self, batteries):
        shuffle(batteries)
        for battery in batteries:
            print(battery.id)
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

        # Catch error if no connection could be made
        if not self.connection == set():
            self.connection.capacity -= self.output
            # Append reference to houses connected to battery
            self.connection.connectedHouses.append(self)
        else:
            print("Error: House",str(self.id),"COULD NOT BE CONNECTED!")
            self.connection = "NOT CONNECTED!"

        # Sort list with possible connections
        self.possible_connections.sort(key = lambda x: x[1])

    # Makes houses printable
    def __str__(self):
        """Comment like this"""
        if self.connection == set() or self.connection == "NOT CONNECTED!":
            return ("House " + str(self.id) + " at " + str(self.location) + " has an output of " + str(self.output))
        else:
            return ("House " + str(self.id) + " at " + str(self.location) + " has an output of " + str(self.output) + " and is connected to Battery " + str(self.connection.id) + " which is " + str(self.distance) + " meters away at " + str(self.connection.location))

class Battery:

    def __init__(self, x, y, capacity,id):
        self.location = (x,y)
        self.maxCapacity = capacity
        self.capacity = capacity
        self.id = id
        self.connectedHouses = []
        self.costs = 5000

    def showConnections(self):
        print("Battery",self.id,"is connected to:")
        for connection in self.connectedHouses:
            print("House",connection.id)

    def __str__(self):
        return("Remaining capacity of Battery " + str(self.id)+ " : " + str(self.capacity))


class Cable:

    def __init__(self):
        self.costs = 9
        self.connectionBattery = set()
        self.connectionHouse = set()
        self.edge = set()
        self.houseLocation = set()
        self.batteryLocation = set ()

class District:

    def __init__(self, loadedData):
        self.houses = loadedData[0]
        self.batteries = loadedData[1]
        self.cables = set()
        self.costs = set()

    def connectGreedy(self):
        for house in self.houses:
            house.connectNearestBattery(self.batteries)

    def connectRandom(self):
        for house in self.houses:
            house.connectRandom(self.batteries)

    def save(self,name):
        with open("configurations/" + name + ".txt", "w", newline="") as file:
            writer = csv.writer(file, dialect = "excel")
            writer.writerow(["configuration for " + name + " :"])
            writer.writerow([self.costs])
            writer.writerow(["\n"])
            writer.writerow(["---Battery-Stats---"])
            for battery in self.batteries:
                writer.writerow([str(battery)])
            writer.writerow(["\n"])
            writer.writerow(["---House-Stats---"])
            for house in self.houses:
                writer.writerow([str(house)])

    def calculateCosts(self):
        self.costs = calculateCosts(self.houses, self.batteries)
