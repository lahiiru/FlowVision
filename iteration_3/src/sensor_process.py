from multiprocessing.connection import Client
from sensors import *
import logging
import numpy as np

logger = logging.getLogger()


class SensorProcess:
    def __init__(self, index):
        self.distance_sensor = DistanceSR04(24, 26)
        self.index = index
        self.distance = 1
        self.avg = 10

    def run(self):
        while 1:
            try:
                m = []
                for i in range(self.avg):
                    m += [self.distance_sensor.get_real_time_distance_cm()]

                m = np.array(m)
                self.distance = np.average(m)

                logger.debug("creating new client {0}".format(self.index))
                conn = Client(('localhost', 7000+self.index), authkey=b'secret password')
                logger.debug("sending distance {0} from processor {1}".format(self.distance, self.index))
                conn.send(self.distance)
            except Exception as e:
                logger.warn("Error from processor {0}: {0}. Retrying...".format(self.index,e.message))



