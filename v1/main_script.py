# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:23:24 2017

@author: cmnunn
"""
from MCM_v1 import TollBoothModel
import numpy as np
import matplotlib.pyplot as plt

#Time parameter(s)
dt = 0.05 #sec

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
#merge_pts[0] = 100 #feet
#merge_pts[1] = 200

#Right
#merge_pts[2] = 100
#merge_pts[1] = 200

#Centered
merge_pts[0] = 200
merge_pts[2] = 200

#Test
#merge_pts[0] = 500 #feet
#merge_pts[1] = 500
#merge_pts[2] = 500

model = TollBoothModel(550, LANE_WIDTH, B, L, merge_pts, line_pos, dt)

for i in range(600):
    model.step()
    
vehicle_pos = model.datacollector.get_agent_vars_dataframe()
frame = vehicle_pos.loc[100,'AgentID':'Position']
print(frame.values)
for a in frame:
    print(a)
one_car = vehicle_pos.xs(1000, level="AgentID")
xvals = np.zeros(len(one_car))
yvals = np.zeros(len(one_car))
for i in range(len(one_car.values)):
    duple = one_car.values[i][0]
    #print(duple)
    xvals[i] = duple[0]
    yvals[i] = duple[1]
plt.plot(xvals,yvals)
two_car = vehicle_pos.xs(2000, level="AgentID")
xvals = np.zeros(len(two_car))
yvals = np.zeros(len(two_car))
for i in range(len(two_car.values)):
    duple = two_car.values[i][0]
    #print(duple)
    xvals[i] = duple[0]
    yvals[i] = duple[1]
#plt.plot(xvals,yvals)

plt.ion()
fig = plt.figure()
ax = plt.axes(xlim=(0,600),ylim=(0,24))
for i in range(200):
    positions_by_step = vehicle_pos.loc[min(3*i,600),'Agent':'Position']

    for car_id in positions_by_step.index.values:
        car_pos = positions_by_step.loc[car_id,'Position']
        ax.add_artist(plt.Circle(car_pos, 4, fc='r'))

    plt.draw()
    plt.pause(0.0000000001)
    plt.cla()


