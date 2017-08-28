import cv2
from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import datetime
import os


def findPoints(f, x, y, z, theta, phi, eeta):
    A = theta
    B = phi
    C = eeta

    x_bar = f * (x * math.cos(A) + y * math.sin(A)) / (
    -x * math.cos(B) * math.sin(A) + y * math.cos(B) * math.cos(A) + z * math.sin(B))
    z_bar = f * (x * math.sin(B) * math.sin(A) - y * math.sin(B) * math.cos(A) + z * math.cos(B)) / (
    -x * math.cos(B) * math.sin(A) + y * math.cos(B) * math.cos(A) + z * math.sin(B))

    x_star = x_bar * math.cos(C) + z_bar * math.sin(C)
    z_star = -x_bar * math.sin(C) + z_bar * math.cos(C)
    return x_star, z_star

