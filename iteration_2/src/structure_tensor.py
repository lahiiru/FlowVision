from __future__ import print_function
import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage.feature import structure_tensor, structure_tensor_eigvals
import math

frame_rate = 7
selected_line = 350

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
         self.frame_idx = 0
         self.spatio_array=np.empty_like(frame)
         self.ref_point =ref_point


     def getSpatioImage(self,frame):
         self.frame_idx +=1
         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
         if(self.frame_idx > self.height):
             self.spatio_array= np.append(self.spatio_array,[frame[self.ref_point,: ]],axis=0)
             return self.spatio_array[int(-1*self.height):,:]
         else :
             self.spatio_array[self.frame_idx-1,:]=(frame[self.ref_point,:])
             return None
         
class Structure_tensor:
    
    sigma = 0.1
    gray = None
    
    def __init__(self,sigma):
        gray = None
        self.sigma = sigma
        print ('Sigma : ', self.sigma)

    def calcDirection(self, frame, debug=True):
        gray = cv2.equalizeHist(frame)
        Axx, Axy, Ayy = structure_tensor(gray, sigma=self.sigma)
        eH, eL = structure_tensor_eigvals(Axx, Axy, Ayy)
        coef = (eH-eL)/(eH+eL)
        tan2t = (2*Axy)/(Axx-Ayy)
        tan2t[np.isnan(tan2t)]=999999
        t=np.arctan(tan2t)/2
        y_max, x_max = t.shape[:2]


        t = t * 180 / np.pi
        t = 90 - t

        # grid wise mean gradient calculation
        y_max, x_max = t.shape[:2]
        h=15
        w=15
        directions = []
        coordinates = []
        for y in range(0,y_max,h):
            for x in range(0,x_max,w):
                roi_t = t[y:y+h, x:x+w]
                roi_eigen = coef[y:y+h, x:x+w]
                data = roi_t.ravel()
                binMean = np.mean(data)
                directions += [binMean]
                coordinates += [(x,y)]
                c = np.mean(roi_eigen)


        plt.clf()
        hist = plt.hist(directions, np.arange(0,90,0.1));
        
        maxBinUpper = np.argmax(hist[0])
        globalDirection = (hist[1][maxBinUpper+1]+hist[1][maxBinUpper])/2

        if debug:
            plt.xlabel('mode = '+str(globalDirection)+'deg, sigma='+str(self.sigma))
            plt.vlines([globalDirection], 0, 100, label = str(globalDirection))
            plt.pause(0.001)

        # visualising
        i = 0
        gray = np.absolute(gray)
        gray = np.uint8(gray)
        vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for x1, y1 in coordinates:
            angle = (90.0-directions[i])*np.pi/180.0
            i+=1
            x2 =  int(round(math.ceil(x1 + 10.0 * np.cos(angle)),0))
            y2 =  int(round(math.ceil(y1 + 10.0 * np.sin(angle))))
            cv2.line(vis, (x1, y1), (x2, y2), (0,255,0), 1, cv2.LINE_AA )

        print ("Structure tensor says: ",globalDirection)
        return vis

def main():
    import sys
    try:
        video_src = sys.argv[1]
        if video_src.isdigit():
            video_src = int(video_src)
    except:
        video_src = "../../03.mp4"
    
    c = cv2.VideoCapture(video_src)
    
    rect, frame = c.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC);
    sp = Spatio(frame,200)
    try:
         sigma = float(sys.argv[2])
    except:
         sigma = 10
            
    st = Structure_tensor(sigma)
    
    while(1):
        rect, frame = c.read()
        if not rect:
            cv2.destroyAllWindows()
            break
        #small_img = cv2.resize(frame,None,fx=0.75, fy=0.75, interpolation = cv2.INTER_CUBIC);
        spatio_image = sp.getSpatioImage(frame)
        #spatio_image = sp.getSpatioImage(small_img)
        print ('Frame index : ' ,sp.frame_idx)
        
        if(sp.frame_idx > sp.height):
             vis = st.calcDirection(spatio_image, False)
             #cv2.imshow('spatio window', spatio_image)
             #cv2.imshow('lines', vis)
        
        #cv2.imshow('preview window', frame)
          
        ch = cv2.waitKey(int(1000.0/frame_rate))
        
        if ch == 27:
            break

if __name__ == '__main__':
    main()


