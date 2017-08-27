import numpy as np
import cv2

# class for get the spatio image from a image sequence
# This contains a continuously growing array (some time it will cause an error)

class Spatio :
     height=0
     width=0
     c=0
     frame_idx=0
     ref_point=0
     spatio_array=[]

     def __init__(self,frame,ref_point):
         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         self.height,self.width=frame.shape
         #self.height=480
         #self.width=480
         self.frame_idx = 0
         self.spatio_array=np.empty_like(frame)
         self.ref_point =ref_point


     # return the grayscale spatio image if it has enough frames
     # to make the spatio image otherwise return None
     def getSpatioImage(self,frame):
         self.frame_idx +=1
         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         if(self.frame_idx > self.height):
             self.spatio_array= np.append(self.spatio_array,[frame[self.ref_point,: ]],axis=0)
             return self.spatio_array[int(-1*self.height):,:]
         else :
             self.spatio_array[self.frame_idx-1,:]=(frame[self.ref_point,:])
             return None
