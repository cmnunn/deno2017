# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:23:24 2017

@author: cmnunn
"""
from MCM_v1 import TollBoothModel
import numpy as np

#Time parameter(s)
dt = 0.01 #sec

# Map parameters
B = 2 #2 booths
L = 1 #1 exit lane
LANE_WIDTH = 12 #feet
LANE_SPACING = 0 #feet
merge_pts = np.zeros(2*B-1)

#Left
merge_pts[0] = 10 #feet
merge_pts[1] = 20
#Right
#merge_pts[2] = 10
#merge_pts[1] = 20
#Centered
#merge_pts[0] = 20
#merge_pts[2] = 20

model = TollBoothModel(100, LANE_WIDTH, LANE_SPACING, B, L, merge_pts, dt)