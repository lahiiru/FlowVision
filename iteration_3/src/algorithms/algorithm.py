class Algorithm:

    def __init__(self):
        self.debug = True

    def compare(self, current_frame, prev_frame, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")