# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:11:55 2017

@author: cmnunn
"""
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from scipy import integrate
import random as rng
from math import floor,ceil
#import numpy as np

class Map(ContinuousSpace):
    """Space of the toll plaza, with defined lanes & bounds"""
    def __init__(self, width, LANE_WIDTH, B, lanes, merge_pts, line_pos):
        super().__init__(width, B*LANE_WIDTH, False)
        self.LANE_WIDTH = LANE_WIDTH
        self.B = B #number of booths
        self.line_pos = line_pos
        self.merge_pts = merge_pts
        self.lanes = lanes

class Booth(Agent):
    """Spawns vehicles according to control algorithms"""
    def __init__(self, lane, model):
        super().__init__(lane, model)
        self.count = 0
        self.queue = 0
        self.time = 0
        self.wait_time = 3 #sec
        self.vel = 0
        
    def open_gate(self):
        if not self.queue or self.time > 0:
            return
        lane = self.unique_id
        v = Vehicle(lane*1000+self.count, self.model, self.vel, 2*(lane-1))
        self.model.schedule.add(v)
        self.model.map.place_agent(v, (0,self.pos[1]))
        self.time = self.wait_time
        self.queue -= 1
        self.count += 1
        
    def take_toll(self):
        if not self.queue:
            return
        self.time -= self.model.dt
        
    def get_y(self):
        return self.y
        
    def get_vel(self):
        return self.vel
        
class EZPass(Booth):
    """Booth that spawns vehicles at full speed, no wait time"""
    def __init__(self, lane, model):
        super().__init__(lane, model)
        self.wait_time = 0
        self.vel = 60*1.46667
        

class Vehicle(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, vel, line):
        super().__init__(unique_id, model)
        #physical attributes
        self.id = unique_id
        self.width = 6 #feet
        self.length = 15 # feet
        self.max_speed = 60*1.46667 #feet/sec
        self.accel = 6.6 #feet/sec^2
        self.decel = 6.6
        self.merge_vel = 4*1.46667
        
        #state attributes
        self.line = line
        self.goal = line
        self.goal2 = line
        self.merging = False
        self.x_vel = vel
        self.y_vel = 0
        
    def brake(self):
        #decrease velocity
        dt = self.model.dt
        self.x_vel = max(self.x_vel - self.decel*dt,0)
        
    def accelerate(self):
        #increase velocity
        dt = self.model.dt
        self.x_vel = min(self.x_vel + self.accel*dt,self.max_speed)
        
    def get_new_goal(self,stop_dist):
        arr = self.model.map.merge_pts
        #lanes = self.model.map.lanes
        neighbors = [None if self.line < 2 else self.line-2, \
                   None if self.line < 1 else self.line-1, \
                   None if self.line >= len(arr)-2 else self.line+1, \
                   None if self.line >= len(arr)-1 else self.line+2]
        #print(neighbors)
        options = []
        for option in neighbors:
            if option != None:
                options.append(option)
        #print(options)
        final = []
        best = arr[self.line]
        for option in options:
            if arr[option] >= best:
                best = arr[option]
        for option in options:
            if arr[option] == best:
                final.append(option)
        self.goal = rng.choice(final)
        
    def merge(self,lag_car,lead_car):
        x = self.pos[0]
        y = self.pos[1]
        if self.merging:
            arr = self.model.map.line_pos
            if abs(y-arr[self.goal]) <= 0.5:
                self.line = self.goal
                self.model.map.place_agent(self, (x,arr[self.line]))
                self.y_vel = 0
                self.merging = False
        else:
            safe = True
            if lead_car.x_vel - self.x_vel < -10:
                if lead_car.pos[0] - lead_car.length - x < 27:
                    safe = False
            elif lag_car != self and x - self.length - lag_car.pos[0] < 8:
                safe = False
            elif lead_car != self and lead_car.pos[0] - lead_car.length - x < 20:               
                safe = False
            if safe:
                direction = 2*(self.line < self.goal)-1
                self.y_vel = direction*self.merge_vel
                self.merging = True
            else:
                self.brake()
                
    def move(self):
        dt = self.model.dt
        x = self.pos[0]
        y = self.pos[1]
        try:
            self.model.map.move_agent(self, (x+dt*self.x_vel,y+dt*self.y_vel))
        except Exception:
            self.model.schedule.remove(self)
    
    def step(self): 
        x = self.pos[0]
        stop_time = self.x_vel/self.decel
        stop_dist = self.x_vel*stop_time/2
        lane_end = self.model.map.merge_pts[self.line]
        #if lane is ending
        if self.merging or 0 < lane_end <= x + 2*stop_dist:
            self.get_new_goal(stop_dist) #update goal
            #if safe, merge
            lead_car = self
            lag_car = self
            for car in self.model.schedule.agents:
                if isinstance(car,Vehicle) and car.unique_id != self.unique_id:
                    if car.line == self.goal or \
                        car.merging and car.goal == self.goal:
                            if x < car.pos[0]:
                                if lead_car.unique_id != self.unique_id:
                                    if car.pos[0] < lead_car.pos[0]:
                                        lead_car = car
                                else:
                                    lead_car = car
                            elif x > car.pos[0]:
                                if lag_car.unique_id != self.unique_id:
                                    if car.pos[0] > lag_car.pos[0]:
                                        lead_car = car
                                else:
                                    lag_car = car
            self.merge(lag_car,lead_car)
            if not self.merging and lane_end <= x + stop_dist + 1:
                self.brake()
        #else:
        blocked = False
        for car in self.model.schedule.agents:
            if isinstance(car,Vehicle) and car.unique_id != self.unique_id:
                if car.line == self.line or \
                    (car.merging and car.goal == self.line):
#                            if 0 < (car.pos[0] - x - 2*car.length + car.x_vel*stop_time) \
                        if 0 < (car.pos[0] - x - car.length) <= stop_dist + 1 - car.x_vel*stop_time/4:
                            blocked = True
                            break
        if blocked:
            self.brake()
        elif self.goal == self.line or self.merging:
            self.accelerate()
        self.move()
        

        
def traffic_arrival(model):
    #time = model.schedule.steps
    total_count = 0
    total_queue = 0
    for agent in model.schedule.agents:
        if isinstance(agent,Booth):
            if rng.random() > 0.99:
                agent.queue += 1
            total_count += agent.count
            total_queue += agent.queue
    return total_count
    
def merging_vehicle_count(model):
    return model.schedule.get_agent_count() - model.map.B
    
def calc_capacity(model,merge_pts,lanes,width):
    test = Vehicle(0,model,0,-1)
    L = (test.max_speed**2)/(2*test.accel)
    K1 = lambda x : 1/(test.length + 2*(2*test.accel*x)**0.5)
    total = 0
    for line in range(len(lanes)):
        if lanes[line]:
            l = min(merge_pts[line],width)
            if line == 0 or line % 2 == 1 \
            or (line % 2 == 0 and not lanes[line-1]):
                total += integrate.quad(K1,0,min(l,L))[0]
                total += max(0,l-L)/(test.length+2*test.max_speed)
    return total

class TollBoothModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, LANE_WIDTH, B, lanes, merge_pts, line_pos, dt, double):
        self.dt = dt
        self.time = 0
        self.map = Map(width,LANE_WIDTH,B,lanes,merge_pts,line_pos)
        self.schedule = BaseScheduler(self)
        self.capacity = floor(calc_capacity(self,merge_pts,lanes,width))-ceil(B/2)
        if double:
            self.capacity = 2*self.capacity
        
        # Create booths
        for i in range(1,B+1):
            b = Booth(i, self)
            self.schedule.add(b)
            self.map.place_agent(b, (0,(i-1/2)*LANE_WIDTH))
        
        self.datacollector = DataCollector(
            model_reporters={"Current Car Count": merging_vehicle_count,
                             "Cumulative Car Count": traffic_arrival},
            agent_reporters={"Position": lambda v: v.pos})

    def step(self):
        '''Advance the model by one step.'''
        traffic_arrival(self)
        # TollBooth Control Algorithm
        for agent in self.schedule.agents:
            if isinstance(agent,Booth):
                agent.take_toll()
                if merging_vehicle_count(self) <= self.capacity or \
                agent.unique_id % 2 == 1:
                    agent.open_gate()
        self.datacollector.collect(self)        
        self.schedule.step()
        self.time += self.dt

