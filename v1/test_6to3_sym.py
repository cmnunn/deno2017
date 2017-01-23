# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:23:24 2017

@author: cmnunn
"""
from MCM_69007 import *
import numpy as np
import matplotlib.pyplot as plt
import math

#Time parameter(s)
dt = 0.05 #sec

# Map parameters
B = 6 #6 booths
L = 3 #3 exit lanes
LANE_WIDTH = 12 #feet
merge_pts = np.zeros(2*B-1)
line_pos = np.zeros(2*B-1)
lanes = [1,0,1,1,1,1,1,1,1,0,1]
for i in range(2*B-1):
    line_pos[i] = (i+1)*LANE_WIDTH/2
    
#Free (default, comment other cases)

#Left
merge_pts[0] = 100 #feet
merge_pts[1] = 100
merge_pts[2] = 350
merge_pts[3] = float('inf')
merge_pts[4] = 350
merge_pts[5] = float('inf') #feet
merge_pts[6] = 350
merge_pts[7] = float('inf')
merge_pts[8] = 350
merge_pts[9] = 100
merge_pts[10] = 100

track_length = 700

dbl = False

for runCount in range(10):

    model = TollBoothModel(track_length,LANE_WIDTH,B,lanes,merge_pts,line_pos,dt,dbl)

    #Print calculated capacity
    print(calc_capacity(model,merge_pts,lanes,track_length))

    steps = 5000

    for i in range(steps):
        model.step()
 
    count_data = model.datacollector.get_model_vars_dataframe()

    outFile = 'test_6to3_sym/test_6to3_sym_run' + str(runCount) + '.txt'
    wF = open(outFile, 'w')

    for indexVal in count_data.index.values:
        wF.write(str(count_data.loc[indexVal, 'Current Car Count']))
        wF.write('\n')

    wF.close()

frame = vehicle_pos.loc[100,'AgentID':'Position']

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

