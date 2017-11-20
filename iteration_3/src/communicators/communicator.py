from debuggers.debugger import Debugger
import logging
import json

logger = logging.getLogger()


class Communicator:
    def __init__(self):
        pass

    def send_message(self, message):
        raise NotImplementedError("Subclass must implement abstract method")

    def prepare_message_json(self, velocity, level, debugObj):
        raise NotImplementedError("Subclass must implement abstract method")