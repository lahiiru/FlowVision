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
                print("placing receive request by process {0}".format(self.index))
                array = conn.recv()
                print("received {0} to processor {1}".format(len(array),self.index))
                pixel_distances = self.algorithm.bulk_receive(array)
                conn.send(pixel_distances)
                del array
                conn.close()
            except:
                print("error-{0}".format(self.index))