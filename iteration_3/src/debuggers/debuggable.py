

class Debuggable:

    def get_visualization(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_state(self):
        raise NotImplementedError("Subclass must implement abstract method")