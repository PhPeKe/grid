class House:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.output = output
        self.id = id
        self.distance = set()
        self.connection = set()


class Battery:

    def __init__(self, x, y, output,id):
        self.location = (x,y)
        self.capacity = output
        self.id = id
