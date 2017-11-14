# from iteration_3.src.debuggers import Debuggable
from debuggers.debuggable import Debuggable
import Queue
import numpy as np
import matplotlib.pyplot as plt


class Algorithm(Debuggable):

    def __init__(self):
        self.debug = False
        self.pixels_per_second = 0
        self.visualization = None
        self.visualization_mode = 0
        self.pixel_distances = []
        self.history_pixel_distances = Queue.Queue(maxsize=100)
        self.frame_count = 0

    def get_pixels_per_second(self):
        self.calculate_pixels_per_second()
        return self.pixels_per_second

    def get_visualization(self):
        if self.visualization_mode == 0:
            return self.visualization
        elif self.visualization_mode == 1:
            return self.pixel_distances

    def receive_frame(self, frame):
        raise NotImplementedError("Subclass must implement abstract method")

    def update(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def calculate_pixels_per_second(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_name(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_state(self):
        state = {}
        state["type"] = self.get_name()
        state["pixels_per_second"] = self.pixels_per_second
        return state