from velocity_convention import Converter


class DataHandler:
    def __init__(self):
        self.area = 0.000236

    def save_to_file(self, frame_nos, pixels_per_second):

        if not len(frame_nos) == 0:

            self.meters_per_second = round(Converter.convert_meters_per_second(pixels_per_second), 2)
            self.discharge = round(self.meters_per_second * self.area * 1000000, 2)

            for i in range(len(frame_nos)):
                print (str(frame_nos[i]) + '\t' + str(self.discharge))