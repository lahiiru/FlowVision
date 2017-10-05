from iteration_3.src.debuggers import Debuggable


class Algorithm(Debuggable):
    def __init__(self):
        self.debug = False
        self.pixels_per_second = 0
        self.visualization = None
        self.tag='Frame'
        self.visualization_mode = 0
        self.matched_points = []

    def get_pixels_per_second(self):
        return self.pixels_per_second

    def get_visualization(self):
        if self.visualization_mode == 0:
            return self.visualization,self.tag
        elif self.visualization_mode == 1:
            return self.matched_points

    def receive_frame(self, frame,tag):
        raise NotImplementedError("Subclass must implement abstract method")

    def update(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")
