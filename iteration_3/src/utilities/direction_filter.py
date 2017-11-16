import Queue
import numpy as np
import matplotlib.pyplot as plt


class DirectionFilter:

    plt.rcParams["figure.figsize"]=(40,3)
    def __init__(self):
        self.points = Queue.Queue(maxsize=500)
        self.directions = Queue.Queue(maxsize=10)
        self.no_of_points = 0
        self.good_point = False
        self.direction_interval = (0, 0)

    def update(self, point):
        self.points.put(point)
        self.no_of_points += 1


        if point is not None:
            # plt.ylim(20, 80)
            # plt.xlim(0,600)
            plt.scatter(point[0], point[1], s=2)
            plt.pause(0.01)



        # if self.no_of_points == 100:
        #     self.no_of_points = 0
        #     self.analyze_histogram()

    def analyze_histogram(self):
            polar = []
            bin_size = 5
            for i in range(100):
                point = self.points.get()
                polar.append(np.rad2deg(np.arctan2(point[1], point[0])))

            # plt.hist(polar, np.arange(-180, 180, bin_size))
            # plt.show()

            hist = np.histogram(polar, np.arange(-180, 180, bin_size))
            maxBinUpper = np.argmax(hist[0])
            direction = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0
            self.direction_interval = (direction-bin_size, direction+bin_size)

    def check_good_point(self, point):
        polar = np.rad2deg(np.arctan2(point[1], point[0]))
        if self.direction_interval[0] <= polar <= self.direction_interval[1]:
            return True
        return False