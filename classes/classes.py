class House:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.output = output
        self.id = id
        self.distance = set()
        self.connection = set()

    def manhattan(self, battery):
        distance = 0
        for h,b in self.location, battery.location:
            distance += abs(h-b)
        self.distance = distance

class Battery:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.capacity = output
        self.id = id
