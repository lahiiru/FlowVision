from distance_sensor import DistanceSensor


class DistanceOneFeet(DistanceSensor):
    def get_real_time_distance_cm(self):
        return 30