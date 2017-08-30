import numpy as np
import cv2

# class for build the spatio temporal image
class STIBuilder:
    height = 0
    width=0
    ref_point = 0
    spatio_image = []
    history_ratio = 0.6
    index = -1
    scale_factor = 2
    array_size =0
    first_round = True
    next_index = 0
    initial_spatio=False
    is_configured=False
    partition_count=0
    new_frame_count=0 # new_frame_count is 0 only if  correct spatio image constructed with correct history and new frame count. new_frame_count >0 for other return values


    def __init__(self,ref_point,history_ratio,scale_factor):
        self.ref_point = ref_point
        self.history_ratio= history_ratio
        self.scale_factor= scale_factor

    def initConfiguration(self, frame):
        self.height = frame.shape[0]
        self.width=frame.shape[1]
        self.array_size = self.height * self.scale_factor
        self.spatio_image = np.zeros((self.array_size, self.width), dtype=np.int)
        self.next_index = self.height - 1
        self.history_count = int(self.history_ratio * self.height)
        self.partition_count = self.height - self.history_count
        self.is_configured = True

    def buildImage(self, frame):
        if(not self.is_configured) :
            self.initConfiguration(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.new_frame_count +=1

        self.index = (self.index + 1) % self.array_size
        self.spatio_image[self.index, :] = frame[self.ref_point,:]
        if self.first_round:

            if (self.index == self.array_size - 1):
                self.first_round = False

            if (self.index == self.height - 1):
                self.next_index = self.index + self.partition_count
                self.initial_spatio= True
                self.new_frame_count=0
                return self.spatio_image[:self.index + 1, ]

            elif self.index < self.height - 1 :
                # do not build the full image (no enough frames) returns what have in tha spatio_image array
                return self.spatio_image[:self.index + 1, ]

            elif (self.index > self.height and self.index == self.next_index):
                self.next_index = (self.index + self.partition_count) % self.array_size
                # print str(self.index) + " next index" + str(self.next_index)
                self.new_frame_count = 0
                return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]
            else:
                # returns the full image but not contains the correct amount of new frames (no enough new frames yet)
                # self.index < self.next_index
                return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]


        else:
            if self.next_index == self.index:
                self.new_frame_count=0
                self.next_index = (self.index + self.partition_count) % self.array_size
                # print str(self.index) + " next index" + str(self.next_index)
                if self.index < self.height - 1:
                    return np.concatenate((self.spatio_image[-(self.height - self.index - 1):, ], self.spatio_image[:self.index + 1, ]),
                                         axis=0)

                else:
                    return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]
            else :
                # returns the full image but not contains the correct amount of new frames (no enough new frames yet)
                # self.index < self.next_index
                if self.index < self.height - 1:
                    return np.concatenate(
                        (self.spatio_image[-(self.height - self.index - 1):, ], self.spatio_image[:self.index + 1, ]),
                        axis=0)

                else:
                    return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]





