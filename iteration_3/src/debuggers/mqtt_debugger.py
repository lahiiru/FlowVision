import json


class MQTTDebugger:

    def __init__(self):
        pass

    @staticmethod
    def get_state_json(self):
        state = {}
        state['camera'] = self.device.camera.get_state()
        state['algorithm'] = self.device.algorithm.get_state()
        return json.dumps(state)