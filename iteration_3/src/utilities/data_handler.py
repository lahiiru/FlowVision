from velocity_convention import Converter
import math

class DataHandler:
    def __init__(self):
        self.area = 0.000236
        self.resultant = 0

    def save_pixel_velocity(self, frame_nos, pixels_per_second):

        if not len(frame_nos) == 0:
            self.meters_per_second = round(Converter.convert_meters_per_second(pixels_per_second), 2)
            self.discharge = round(self.meters_per_second * self.area * 1000000, 2)

            for i in range(len(frame_nos)):
                print (str(frame_nos[i]) + '\t' + str(self.discharge))

    def save_pixel_distances(self,  frame_nos, x_distances, y_distances):

        if not len(frame_nos) == 0:
            for i in range(len(x_distances)):
                # self.resultant = round(math.sqrt(
                # math.pow(x_distances[i], 2) + math.pow(y_distances[i], 2)), 2)
                # print (str(frame_nos[i]) + '\t' + str(self.resultant))
                print (str(x_distances[i]) + '\t' + str(y_distances[i]))

    def save_pixel_distance_validated(self, frame_nos, x , y):

        if not len(frame_nos) == 0:
            self.resultant = round(math.sqrt(
                math.pow(x, 2) + math.pow(y, 2)), 2)

            for i in range(len(frame_nos)):
                print (str(frame_nos[i]) + '\t' + str(self.resultant))
