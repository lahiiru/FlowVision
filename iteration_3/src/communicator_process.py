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

            conn = Client(('localhost', 7000+self.index), authkey=b'secret password')
            message = conn.recv()
            conn.close()
            print("received length {0} to processor {1}".format(len(message),self.index))
            ret = "0"
            while ret == "0":
                ret = self.communicator.send_message(message)
                print ("received response from server {0} to processor {1}".format(ret, self.index))
                if ret == "0":
                    print "update failed retrying..."


