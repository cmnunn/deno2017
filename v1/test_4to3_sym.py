# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:23:24 2017

@author: cmnunn
"""
from MCM_69007 import *
import numpy as np
import matplotlib.pyplot as plt

#Time parameter(s)
dt = 0.05 #sec

# Map parameters
B = 4 #4 booths
L = 3 #3 exit lanes
LANE_WIDTH = 12 #feet
# Array of lane ending points
merge_pts = np.zeros(2*B-1)
# Array of lane location on the y-axis
line_pos = np.zeros(2*B-1) 
for i in range(2*B-1):
    line_pos[i] = (i+1)*LANE_WIDTH/2
# Array of lanes (0 for junctions that lie halfway between lanes, 1 otherwise)
lanes = [1,1,1,1,1,1,1]
    

#Merge points for 4 lane, symmetric merge to 3 lanes
merge_pts[0] = 200 #feet
merge_pts[1] = float('inf')
merge_pts[2] = 200
merge_pts[3] = float('inf')
merge_pts[4] = 200
merge_pts[5] = float('inf')
merge_pts[6] = 200

track_length = 400

dbl = False

for runCount in range(10):

    model = TollBoothModel(track_length,LANE_WIDTH,B,lanes,merge_pts,line_pos,dt,dbl)

    #Print calculated capacity
    print(calc_capacity(model,merge_pts,lanes,track_length))

    #5000 timesteps
    steps = 5000

    for i in range(steps):
        model.step()
 
    count_data = model.datacollector.get_model_vars_dataframe()
    outFile = 'test_4to3_sym/test_4to3_sym_run' + str(runCount) + '.txt'
    wF = open(outFile, 'w')

    for indexVal in count_data.index.values:
        wF.write(str(count_data.loc[indexVal, 'Current Car Count']))
        wF.write('\n')

    wF.close()

#plt.ion()
#fig = plt.figure()
#ax = plt.axes(xlim=(0,model.map.width),ylim=(0,model.map.height))
#plot_rate = 4
#for i in range(math.floor(steps/plot_rate)):
#    positions_by_step = vehicle_pos.loc[min(plot_rate*i,steps),'Agent':'Position']
#
#    for car_id in positions_by_step.index.values:
#        car_pos = positions_by_step.loc[car_id,'Position']
#        color = 'r'
#        if car_id < B*2000:
#            color = 'b'
#        ax.add_artist(plt.Rectangle(car_pos, 15, 6, fc=color))
#
#    plt.draw()
#    plt.pause(0.0000000001)
#    plt.cla()

