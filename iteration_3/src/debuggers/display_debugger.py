from debugger import AbstractDebugger
import cv2


class DisplayDebugger(AbstractDebugger):

    def __init__(self, device):
        AbstractDebugger.__init__(self, device)

    def run(self):

        if self.device.algorithm.debug:
            while True:
                frame = self.device.camera.get_frame()
                if frame is not None:
                    self.device.algorithm.receive_frame(frame)
                    self.device.algorithm.update()
                    vis = self.device.algorithm.get_visualization()
                    if vis is not None:
                        cv2.imshow('video', vis)
                        cv2.waitKey(1000/self.device.camera.frame_rate)

                else:
                    cv2.destroyAllWindows()
                    break