import cv2
from cv2 import *
from iteration_3.src.algorithms.piv import piv_algorithm

try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = "..\\..\\01.mp4"


pivInstance = piv_algorithm.PIVAlgorithm()
pivInstance.debug=True
c = cv2.VideoCapture(video_src)

rect, prev = c.read()
print prev.shape
while (1):
    rect, frame = c.read()
    if not rect:
        break

    pivInstance.receive_frame(frame)
    pivInstance.update()
