from piv_algorithm import *


class ColorChannelsPIV(ParticleImageVelocimetryAlgorithm):
    def __init__(self):
        ParticleImageVelocimetryAlgorithm.__init__(self, 7)

    def receive_frame(self, frame):
        pass

    def _process_pre_filters(self):
        pass

    def _calculate_template_bounds(self, frame):
        bounds = []
        return bounds

    def _template_qa_passed(self, template):
        return True
