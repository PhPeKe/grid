from functions.manhattan import manhattan

class Battery:

    def __init__(self, x, y, capacity,id):
        self.location = (x,y)
        self.maxCapacity = capacity
        self.capacity = capacity
        self.id = id
        self.connectedHouses = []
        self.costs = 5000
        self.totalDistance = set()

    def totalDistance(self):
        self.totalDistance = 0
        for house in self.connectedHouses:
            self.totalDistance += house.distanc

    def showConnections(self):
        print("Battery",self.id,"is connected to:")
        for connection in self.connectedHouses:
            print("House",connection.id)

    # Changing location
    def changeLocation(self, location):
        self.location = location

        # Change distance when battery is moved
        for house in self.connectedHouses:
            house.distance = manhattan(house, self)

    def __str__(self):
        return("Remaining capacity of Battery " + str(self.id)+ " : " + str(self.capacity))
