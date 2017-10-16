from MQTTBroker import MQTTBroker
from iteration_3.src.debuggers.mqtt_debugger import MQTTDebugger
import json
import time
import threading


class Communicator(threading.Thread):

    broker = MQTTBroker()
    client = broker.getClient()

    def __init__(self):
        self.loopCount = 0

    def send(self):
        debugObj = MQTTDebugger.get_state_object()
        reported = dict()
        reported["velocity"] = 0
        reported["level"] = 0
        reported["debug"] = debugObj

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
