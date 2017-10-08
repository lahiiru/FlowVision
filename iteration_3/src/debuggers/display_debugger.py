from debugger import AbstractDebugger
import cv2
import matplotlib.pyplot as plt


class DisplayDebugger(AbstractDebugger):

    def __init__(self, device):
        AbstractDebugger.__init__(self, device)

    def run(self):

        if self.device.algorithm.debug:

            if self.device.algorithm.visualization_mode == 0:
                while True:
                    vis = self.device.algorithm.get_visualization()
                    if vis is not None:
                        cv2.imshow('frame', vis)
                        # cv2.waitKey(0)
                        cv2.waitKey(1000/self.device.camera.frame_rate)

                    # else:
                    #     cv2.destroyAllWindows()
                    #     break

            elif self.device.algorithm.visualization_mode == 1:
                while True:
                    point = self.device.algorithm.get_visualization()
                    if point is not None and len(point)>0:
                        plt.scatter(*zip(*point), s=2)
                        plt.pause(0.01)