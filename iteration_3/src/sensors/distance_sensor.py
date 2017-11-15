

class DistanceSensor:

    def __init__(self):
        self.max_distance = 500
        self.min_distance = 0

    def get_real_time_distance_cm(self):
        raise NotImplementedError("Subclass must implement abstract method")