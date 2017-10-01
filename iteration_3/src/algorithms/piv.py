from algorithm import Algorithm


class PIVAlgorithm (Algorithm) :

    def __init__(self):
        Algorithm.__init__(self)

    def compare(self, current_frame, prev_frame, **kwargs):
        print 'child'