class house:

    def __init__(self, x, y, output):
        self.location = (x,y)
        self.output = output
        self.id = set()
        self.distance = set()
        self.connection = set()
