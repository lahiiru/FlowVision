import matplotlib.pyplot as plt


class DirectionFilter:

    def __init__(self):
        self.direction = []
        self.debug = False

    def update(self, points):
        self.direction.append(points)

