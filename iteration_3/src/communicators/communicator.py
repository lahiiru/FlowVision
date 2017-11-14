from communicators.MQTTBroker import MQTTBroker
from debuggers.debugger import Debugger
import json
import time
from threading import Thread
import logging

logger = logging.getLogger()


class Communicator(Thread):


    def __init__(self):
        Thread.__init__(self)


    def send(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def run(self):
        while True:
            self.send()
            time.sleep(5)
