from functions.manhattan import manhattan
class House:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.output = output
        self.id = id
        self.distance = 1000
        self.connection = set()

    # Provides an overview of the houses values and connections if present
    def overview(self):
        if self.connection == set():
            print("House",self.id,"at",self.location,"has an output of",self.output)
        else:
            print("House",self.id,"at",self.location,"has an output of",self.output,"and is connected to Battery",self.connection.id, "which is", self.distance,"meters away at",self.connection.location)

    # Greedy algorithm that connects houses to nearest battery
    def connectNearestBattery(self, batteries):
        for battery in batteries:
            distance = manhattan(self, battery)
            if distance < self.distance and battery.capacity > self.output:
                self.distance = distance
                self.connection = battery
                connectedBattery = battery
                battery.capacity -= self.output
                print("Remaining capacity of battery",battery.id,":",battery.capacity)
        connectedBattery.connectedHouses.append(self)

class Battery:

    def __init__(self, x, y, capacity,id):
        self.location = (x,y)
        self.capacity = capacity
        self.id = id
        self.connectedHouses = []
        self.costs = 5000

    def showConnections(self):
        print("Battery",self.id,"is connected to:")
        for connection in self.connectedHouses:
            print("House",connection.id)

    def showCapacity(self):
        print("Remaining capacity:",self.capacity)

class Cable:

    def __init__(self):
        self.costs = set()
        self.connection_battery = set()
        self.connection_house = set()
        self.edge = set()
