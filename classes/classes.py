class House:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.output = output
        self.id = id
        self.distance = 1000
        self.connection = set()

    def manhattan(self, batteries):
        for battery in batteries:
            distance = abs(self.location[0] - battery.location[0]) + abs(self.location[1] - battery.location[1])
            print("distance battery ", battery.id, distance)
            if distance < self.distance:
                self.distance = distance
                self.connection = battery

class Battery:

    def __init__(self, x, y, capacity,id):
        self.location = (x,y)
        self.capacity = capacity
        self.id = id

class Cable:

    def __init__(self):
        self.costs = set()
        self.connection_battery = set()
        self.connection_house = set()
        self.edge = set()
