from multiprocessing.connection import Client
from algorithms import *
import numpy as np
import time


class Processor:
    def __init__(self, index):
        self.algorithm = PIVThreeFramesAlgorithm(25)
        self.algorithm.debug = False
        self.algorithm.visualization_mode = 0
        self.index = index

    def run(self):
        while 1:
            try:
                conn = Client(('localhost', 7000+self.index), authkey=b'secret password')
                array = conn.recv()
                print("received {0} to processor {1}".format(len(array),self.index))
                for f in array:
                    self.algorithm.receive_frame(f)
                    self.algorithm.update()
                conn.send(self.algorithm.get_pixels_per_second())
                del array
                conn.close()
            except:
                print("error-{0}".format(self.index))