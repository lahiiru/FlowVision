from MQTTBroker import MQTTBroker
from iteration_3.src.debuggers.debugger import Debugger
import json
import time
from threading import Thread
import logging
from iteration_3.src.communicator.communicator import Communicator

logger = logging.getLogger()


class AWSCommunicator(Communicator):


    def __init__(self):
        Thread.__init__(self)
        self.broker = MQTTBroker()
        self.client = self.broker.getClient()
        self.loopCount = 0

    def send(self):

        reported = dict()
        reported["velocity"] = 0
        reported["level"] = 0

        try:
            debugObj = Debugger.get_state_object()
            reported["debug"] = debugObj
        except:
            logger.warn("couldn't get state object from debugger")

        state = dict()

        state["reported"] = reported

        message = dict()

        message["state"] = state

        m = json.dumps(message)

        self.client.publish("$aws/things/FlowMeter-local/shadow/update", m, 1)
        self.loopCount += 1

    def run(self):
        while True:
            self.send()
            time.sleep(5)
