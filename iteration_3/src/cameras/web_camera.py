from camera import AbstractCamera
import cv2


class WebCamera(AbstractCamera):

    def run(self):
        cap = cv2.VideoCapture(0)
        frame_height, frame_width = 640, 480  # 2048, 1536 or 640, 480

        # say cameras to adjust resolution
        cap.set(3, frame_width)
        cap.set(4, frame_height)
        # see whether cameras has adjusted the resolution
        print (cap.get(3), cap.get(4))

        while True:
            r, img = cap.read()
            self._put_frame(img)