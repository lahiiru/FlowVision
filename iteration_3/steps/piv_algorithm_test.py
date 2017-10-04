import cv2
from cv2 import *
from iteration_3.src.algorithms.piv import piv_algorithm

try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = "..\\..\\01.mp4"


piv_instance = piv_algorithm.ParticleImageVelocimetryAlgorithm()
piv_instance.debug=True
c = cv2.VideoCapture(video_src)

rect, prev = c.read()
while (1):
    rect, frame = c.read()
    if not rect:
        break
    piv_instance.receive_frame(frame)
    piv_instance.update()

