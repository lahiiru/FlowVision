class MQTTDebugger:

    def __init__(self):
        pass

    @staticmethod
    def get_state_object(self):
        state = {}
        state['camera'] = self.device.camera.get_state()
        state['algorithm'] = self.device.algorithm.get_state()
        return state