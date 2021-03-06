# USAGE
# python fps_demo.py -d 1 -n 100
# python fps_demo.py --display 1

# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-real_frames", type=int, default=100,
	help="# of real_frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not real_frames should be displayed")
args = vars(ap.parse_args())


# created a *threaded *video stream, allow the camera senor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED real_frames from webcam...")
vs = WebcamVideoStream(src=1).start()
fps = FPS().start()
  
i = 0
# loop over some real_frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	i+=1
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		cv2.imwrite('./fps/'+str(i)+'.jpg',frame)
		
	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
