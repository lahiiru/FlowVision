from multiprocessing.connection import Client
from communicators import *
import logging

logger = logging.getLogger()


class CommunicatorProcess:
    def __init__(self, index):
        self.communicator = ThingspeakCommunicator()
        self.index = index

    def run(self):
        while 1:
            try:
                logger.debug("creating new client {0}".format(self.index))
                conn = Client(('localhost', 7000+self.index), authkey=b'secret password')
                logger.debug("placing receive request by process {0}".format(self.index))
                message = conn.recv()
                logger.debug("received length {0} to processor {1}".format(len(message), self.index))
                conn.close()
                ret = "0"
                while ret == "0":
                    ret = self.communicator.send_message(message)
                    logger.debug("received response from server {0} to processor {1}".format(ret, self.index))
                    if ret == "0":
                        logger.debug("update failed retrying...")
            except Exception as e:
                logger.warn("Error from processor {0}: {0}. Retrying...".format(self.index,e.message))



