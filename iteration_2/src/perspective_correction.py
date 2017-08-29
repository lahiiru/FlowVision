"""
    Prospective projection manual inspection helper

"""
import cv2
import math
import numpy as np
from config import DevConfig

def findPoints(f, x, y, z, theta, phi, eeta):
    """
        3D real world to 2D image plane projection

        :param f: focal length of camera*
        :param x: real world distance along the horizontal axis parallel to the image plane
        :param y: real world distance along the axis which is perpendicular to the image plane
        :param z: real world distance along the vertical axis parallel to the image plane
        :param theta: camera rotation in degrees around vertical axis
        :param phi: camera rotation in degrees around horizontal axis
        :param eeta: camera rotation in degrees around axis through optical center
        :return: image plane coordinates (image center as the origin) of the projected point (x,y,z)
    """
    A = np.deg2rad(theta)
    B = np.deg2rad(phi)
    C = np.deg2rad(eeta)

    if y==0: y=0.001 # y can't be zero because point can't be on the lense

    x_bar = f * (x * math.cos(A) + y * math.sin(A)) / (
    -x * math.cos(B) * math.sin(A) + y * math.cos(B) * math.cos(A) + z * math.sin(B))
    z_bar = f * (x * math.sin(B) * math.sin(A) - y * math.sin(B) * math.cos(A) + z * math.cos(B)) / (
    -x * math.cos(B) * math.sin(A) + y * math.cos(B) * math.cos(A) + z * math.sin(B))

    x_star = x_bar * math.cos(C) + z_bar * math.sin(C)
    z_star = -x_bar * math.sin(C) + z_bar * math.cos(C)
    return x_star, z_star

def translateToImageCoords(point, center):
    # Translating points to image coordinate system
    x, y = (i + j for i, j in zip(point, center))
    # Checking and constraining into image bounds
    if x < 0: x = 0
    if x > w: x = w
    if y > h: y = h
    # Rounding off to nearest pixel
    x, y = int(x), int(y)
    return x, y

cap = cv2.VideoCapture(DevConfig.WEB_CAM_INDEX)
ret, frame = cap.read()
h, w = frame.shape[:2]
center = w / 2, h / 2
#                                      f  x   y  z  th ph et  (angles in degrees, y is the axis through optical center
rh, rw = 10, 10 # rectangle dimensions
th, ph, et = 0,0,45 # are to determined by accelerometer

p0_ = findPoints(DevConfig.WEB_CAM_F, 0, 300, 0, 0, 0, 0)
p1_ = findPoints(DevConfig.WEB_CAM_F, rw, 300, 0, 0, 0, 0)
p2_ = findPoints(DevConfig.WEB_CAM_F, rw, 300, rh, 0, 0, 0)
p3_ = findPoints(DevConfig.WEB_CAM_F, 0, 300, rh, 0, 0, 0)

p0t_ = findPoints(DevConfig.WEB_CAM_F, 0, 300, 0, th, ph, et)
p1t_ = findPoints(DevConfig.WEB_CAM_F, rw, 300, 0, th, ph, et)
p2t_ = findPoints(DevConfig.WEB_CAM_F, rw, 300, rh, th, ph, et)
p3t_ = findPoints(DevConfig.WEB_CAM_F, 0, 300, rh, th, ph, et)

p0 = translateToImageCoords(p0_,center)
p1 = translateToImageCoords(p1_,center)
p2 = translateToImageCoords(p2_,center)
p3 = translateToImageCoords(p3_,center)

p0t = translateToImageCoords(p0t_,center)
p1t = translateToImageCoords(p1t_,center)
p2t = translateToImageCoords(p2t_,center)
p3t = translateToImageCoords(p3t_,center)

print (p1, h, w)

rect = np.array([p0t, p1t, p2t, p3t],np.float32)
dst = np.array([p0, p1, p2, p3],np.float32)
print (rect)

# transform matrix
T = cv2.getPerspectiveTransform(rect, dst)

while (1):
    ret, frame = cap.read()
    # print frame.shape
    vis = frame
    # marking the center - white
    vis = cv2.circle(vis, center, 2, (255, 255, 255), thickness=2)
    # marking projected point - yellow
    vis = cv2.circle(vis, p1[::-1], 3, (0,255,255), thickness=1)
    warp = cv2.warpPerspective(frame, T, frame.shape[:2][::-1])

    cv2.imshow('frame', vis)
    cv2.imshow('warp', warp)
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

cv2.destroyAllWindows()
cap.release()