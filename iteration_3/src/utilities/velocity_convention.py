import math


class Converter:
    height = 2
    angle_of_view = 54
    width = 640

    def __init__(self):
        pass

    @staticmethod
    def set_system_params(height=2, angle_of_view=54, width=640):
        Converter.height=height
        Converter.angle_of_view=angle_of_view
        Converter.width=width

    @staticmethod
    def convert_meters_per_second(pixels_per_second):
        Converter.speed = (2 * Converter.height * math.tan(math.radians(Converter.angle_of_view / 2)) / Converter.width) * pixels_per_second
        return Converter.speed