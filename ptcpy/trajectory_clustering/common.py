"""
Created on 4. 5. 2015

@author: janbednarik
"""

from math import *


def euclid_dist(p1, p2):
    assert (len(p1) == len(p2))
    return sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))]))
