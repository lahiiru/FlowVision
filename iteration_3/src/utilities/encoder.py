import numpy as np
import logging

logger = logging.getLogger()


class Encoder:

    # no_of_whole_numbers=4
    # no_of_decimal_places=2

    def __init__(self):
        pass

    @staticmethod
    def encode(frame, params):
        if frame is None:
            logger.warn('No frame received for encoding')
            return
        blue_channel = np.zeros_like(frame[0, :, 0])
        value = "{:07.2f}".format(params)  # 4 int positions and 2 decimal positions
        if len(value) > 7:
            frame[0, :, 0] = 0
            logger.warn('Encoding value is outs of bound')
            return frame
        j = 0
        for i in range(len(value)):
            if value[i] == ('.'):
                continue
            blue_channel[j] = int(value[i])
            j += 1

        frame[0, :, 0] = blue_channel

        return frame

    @staticmethod
    def decode(frame):
        if frame is None:
            logger.warn('No frame received for decoding')
            return
        blue_channel = np.copy(frame[0, :, 0])
        value = ''
        for i in range(7):
            if i == 4:
                value += '.'
                continue

            value += str(blue_channel[i])
        value = float(value)

        return frame, value
