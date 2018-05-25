from helpers.manhattan import manhattan

class Battery:
    """Battery.

    Class Battery:
    - Holds all necessary information about a battery:
        -capacity: initiated as maximum capacity but when houses are connected
          their output is deducted
        -maxCapacity: maximum output, never changes
    - Holds a list of all connected houses so they can be accessed from the
      Battery
    """
    def __init__(self, x, y, capacity,id):
        self.location = (x,y)
        self.maxCapacity = capacity
        self.capacity = capacity
        self.id = id
        self.connectedHouses = []
        self.costs = 5000
        self.totalDistance = set()
        self.closestBattery = set()
        self.closestBatteryDistance = set()
        self.batteryType = -1

    def totalDistance(self):
        """Calculates total distance to all connected houses"""
        self.totalDistance = 0
        for house in self.connectedHouses:
            self.totalDistance += house.distanc

    def showConnections(self):
        """Prints out user-friendly output of all connected houses"""
        print("Battery",self.id,"is connected to:")
        for connection in self.connectedHouses:
            print("House",connection.id)

    def changeLocation(self, location):
        """changeLocation.

        Changes the location of the battery and recalculates distance for all
        connected houses.
        """
        self.location = (location[0],location[1])

        # Change distance when battery is moved
        for house in self.connectedHouses:
            house.distance = manhattan(house, self)

    def __str__(self):
        """Returns a nice readable overview when battery object is printed"""
        return("Remaining capacity of Battery " + str(self.id)+ " : " + str(self.capacity))
