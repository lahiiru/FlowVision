import Queue
import numpy as np
import matplotlib.pyplot as plt
from velocity_convention import Converter


class DirectionFilter:

    plt.rcParams["figure.figsize"]=(40,3)

    def __init__(self):
        self.points = Queue.Queue(maxsize=500)
        self.directions = Queue.Queue(maxsize=10)
        self.no_of_points = 0
        self.good_point = False
        self.direction_interval = (0, 0)
        self.area = 0.000236
        self.array = []
        self.no_of_frames = 1000
        self.f = open('DataSet', 'w')

    def update(self, point):
        self.points.put(point)
        self.no_of_points += 1

        if point is not None:
            # plt.ylim(0, 350)
            # plt.xlim(0, 350)

            # pixels_per_second = point[1] * 50
            # self.meters_per_second = round(Converter.convert_meters_per_second(pixels_per_second), 2)
            # self.discharge = self.meters_per_second * self.area * 1000000

            print(point[0])
            # self.array.append([point[0], round(self.discharge*, 2)])

            # self.f.write(str(point[1]))
            # self.f.write('\t')
            # self.f.write(str(point[2]))
            # self.f.write('\n')

            # if point[0] == self.no_of_frames:
            #     self.array = np.array(self.array)
            #     plt.plot(self.array[:,0], self.array[:,1])
            #     plt.pause(0.01)
            #     print (self.array)
            #     self.f.close()


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