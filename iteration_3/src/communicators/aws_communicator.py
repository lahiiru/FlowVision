from MQTTBroker import MQTTBroker
from debuggers.debugger import Debugger
import json
import time
from threading import Thread
import logging
from communicators import Communicator

logger = logging.getLogger()


class AWSCommunicator(Communicator):

    def prepare_message_json(self, velocity, level, debugObj):
        reported = dict()
        reported["velocity"] = velocity
        reported["level"] = level
        reported["debug"] = debugObj

        state = dict()
        state["reported"] = reported
        message = dict()
        message["state"] = state
        m = json.dumps(message)

        return m

    def __init__(self):
        Communicator.__init__(self)
        self.broker = MQTTBroker()
        self.client = self.broker.getClient()

    def send_message(self, message):
        self.client.publish("$aws/things/FlowMeter-local/shadow/update", message, 1)




