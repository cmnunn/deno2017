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
merge_pts = np.zeros(2*B-1)
line_pos = np.zeros(2*B-1)
for i in range(2*B-1):
    line_pos[i] = (i+1)*LANE_WIDTH/2
    
#Free (default, comment other cases)

#Left
#merge_pts[0] = 10 #feet
#merge_pts[1] = 20

#Right
#merge_pts[2] = 10
#merge_pts[1] = 20

#Centered
#merge_pts[0] = 20
#merge_pts[2] = 20

#Test
merge_pts[0] = 500 #feet
merge_pts[1] = 500

model = TollBoothModel(550, LANE_WIDTH, B, L, merge_pts, line_pos, dt)

for i in range(300):
    model.step()
    
vehicle_pos = model.datacollector.get_agent_vars_dataframe()
vehicle_pos.plot()