# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:23:24 2017

@author: cmnunn
"""
from MCM_v1 import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

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

steps = 60

for i in range(steps):
    model.step()


fig = plt.figure()
#define axis limits
ax = plt.axes(xlim=(0,model.map.width),ylim=(0,model.map.height))

# add cars as circles with center 0,0
# radius 4 and fillcolor fc
#car1 = plt.Circle((0,0), 4, fc='r')
#car2 = plt.Circle((0,0), 4, fc='b')
#car3 = plt.Circle((0,0), 4, fc='g')
#car4 = plt.Circle((0,0), 4, fc='y')

# initial placement on plot
#def init():
#    car1.center = (0,6)
#    car2.center = (0,18)
#    car3.center = (0,6)
#    car4.center = (0,18)
#
#    ax.add_patch(car1)
#    ax.add_patch(car2)
#    ax.add_patch(car3)
#    ax.add_patch(car4)
#
#    return car1,car2,car3,car4

# define animation step
# called iteratively
def animate(i):
    # recenter cars 1 and 2 
    # check i to make sure no out of bounds errors
    plt.cla()
    vehicle_pos = model.datacollector.get_agent_vars_dataframe()
    frame = vehicle_pos.loc[i]
    for pos in frame.values:
        #print(pos)
        ax.add_patch(plt.Circle(pos[0], 4, fc='g'))
    #car1.center = one_car.values[min(i,(len(one_car.values)-1))][0] 
    #car2.center = two_car.values[min(i,(len(two_car.values)-1))][0] 
  
    #return car1,car2,car3,car4

anim = animation.FuncAnimation(fig, animate, frames=steps, interval=20, blit=False)

# i think you need ffmpeg installed for this to work
anim.save('basic_animation.mp4', fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()