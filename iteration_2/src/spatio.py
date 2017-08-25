import numpy as np
import cv2
import time
from matplotlib import pyplot as plt


frame_rate = 30
selected_line = 350
history_ratio = 0.6
scale_factor = 2

class Spatio:
    height = 0
    width = 0
    ref_point = 0
    spatio_array = []

    history_ratio = 0.6
    index = -1
    scale_factor = 2
    array_size =0
    first_round = True
    next_index = 0
    initial_spatio=False


    def __init__(self, frame, ref_point,history_ratio,scale_factor):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.height, self.width = frame.shape
        self.array_size = self.height * scale_factor
        self.spatio_array = np.zeros((self.array_size, self.width), dtype=np.int)
        self.ref_point = ref_point
        self.history_ratio= history_ratio
        self.scale_factor= scale_factor
        self.next_index=self.height-1
        self.history_count = int(self.history_ratio * self.height)
        self.partition_count = self.height - self.history_count

    def getSpatioImage(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        self.index = (self.index + 1) % self.array_size
        self.spatio_array[self.index, :] = frame[self.ref_point,:]



        if self.first_round:

            if (self.index == self.array_size - 1):
                self.first_round = False

            if (self.index == self.height - 1):
                self.next_index = self.index + self.partition_count
                self.initial_spatio= True
                return self.spatio_array[:self.index + 1, ]

            if (self.index > self.height and self.index == self.next_index):
                self.next_index = (self.index + self.partition_count) % self.array_size
                print str(self.index) + " next index" + str(self.next_index)
                return self.spatio_array[self.index - (self.height - 1):self.index + 1, ]
            return None

        else:
            if self.next_index == self.index:
                self.next_index = (self.index + self.partition_count) % self.array_size
                print str(self.index) + " next index" + str(self.next_index)
                if self.index < self.height - 1:
                    return np.concatenate((self.spatio_array[-(self.height - self.index - 1):, ], self.spatio_array[:self.index + 1, ]),
                                         axis=0)

                else:
                    return self.spatio_array[self.index - (self.height - 1):self.index + 1, ]
            return None