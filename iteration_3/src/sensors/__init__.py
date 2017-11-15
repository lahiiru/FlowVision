import sys
from distance_one_feet import DistanceOneFeet

c = ['DistanceOneFeet']

if sys.platform == 'linux2':
    from distance_sr04 import DistanceSR04

    c += ['DistanceSR04']

__all__ = c