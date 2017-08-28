"""
    Prospective projection manual inspection helper
    
"""
import cv2
import math
import numpy as np

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


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
h, w = frame.shape[:2]
#               f    x   y   z   th ph et  (angles in degrees, y is the axis through optical center
p = findPoints(1350, 10, 300, 0, 0, 0, 0)
print (p, h,w)
# Translating points to image coordinate system
center = w/2, h/2
x, y = (i+j for i,j in zip(p,center))
# Checking and constraining into image bounds
if x < 0: x = 0
if x > w: x = w
if y > h: y = h
# Rounding off to nearest pixel
x, y = int(x), int(y)

while (1):
    ret, frame = cap.read()
    # print frame.shape
    vis = frame
    # marking the center - white
    vis = cv2.circle(vis, center, 2, (255, 255, 255), thickness=2)
    # marking projected point - yellow
    vis = cv2.circle(vis, (x,y), 3, (0,255,255), thickness=1)
    cv2.imshow('frame', vis)
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

cv2.destroyAllWindows()
cap.release()