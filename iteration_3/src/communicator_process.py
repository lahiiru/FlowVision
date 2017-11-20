from multiprocessing.connection import Client
from communicators import *
import numpy as np
import time


class CommunicatorProcess:
    def __init__(self, index):
        self.communicator = ThingspeakCommunicator()
        self.index = index

    def run(self):
        while 1:
            print("creating new client {0}".format(self.index))
            conn = Client(('localhost', 7000+self.index), authkey=b'secret password')
            print("placing receive request by process {0}".format(self.index))
            message = conn.recv()
            print("received length {0} to processor {1}".format(len(message), self.index))
            conn.close()
            ret = "0"
            while ret == "0":
                ret = self.communicator.send_message(message)
                print ("received response from server {0} to processor {1}".format(ret, self.index))
                if ret == "0":
                    print "update failed retrying..."


