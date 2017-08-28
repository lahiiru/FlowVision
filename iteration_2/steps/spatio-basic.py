#!/usr/bin/env python

'''
    Basic spatio-temporal image creation with ability to choose row interactively
    python spatio-basic.py "fileName"
'''

from __future__ import print_function

import numpy as np
import cv2

mouseX,mouseY = (0,250)

class App:
    def __init__(self, video_src):
        self.fileIdx = 0
        self.cam = cv2.VideoCapture(video_src)
        self.frame_idx = 0
        
    def run(self):
            cv2.namedWindow('vis')
            cv2.setMouseCallback('vis',draw_circle)
            ret, frame = self.cam.read()
            empty = np.empty_like(frame)
            height, width, c = empty.shape
            global mouseY
            mouseY = 250
            while self.cam.isOpened():
                ret, frame = self.cam.read()
                self.fileIdx+=1

                if ret==False:
                    ch = cv2.waitKey(1)
                    if ch == 27:
                            break
                    continue

                self.frame_idx += 1
                self.frame_idx %= height-1
                x = mouseY
                empty[self.frame_idx,:,:] = frame[x,:,:]
                bw = frame
                bw[x,:,:] = np.ones_like(bw[x,:,:])*255

                vis1 = np.hstack((empty,bw))
                cv2.imshow('vis', vis1)

                #cv2.imwrite('sti/'+str(self.fileIdx)+'.jpg', empty)

                ch = cv2.waitKey(1)
                if ch == 27:
                        break

def draw_circle(event,x,y,flags,param):
    global mouseX, mouseY
    if event == 4:
        mouseX, mouseY = x, y
            
def main():
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = '../../01.mp4'

    print(__doc__)
    App(video_src).run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
