from iteration_3.src.debuggers import Debuggable


class Algorithm(Debuggable):
    def __init__(self):
        self.debug = False
        self.pixels_per_second = 0
        self.visualization = None

    def get_pixels_per_second(self):
        return self.pixels_per_second

    def get_visualization(self):
        return self.visualization

    def receive_frame(self, frame):
        raise NotImplementedError("Subclass must implement abstract method")

    def update(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")
