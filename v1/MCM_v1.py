# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:11:55 2017

@author: cmnunn
"""
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
#import random
#import numpy as np

class Map(ContinuousSpace):
    """Space of the toll plaza, with defined lanes & bounds"""
    def __init__(self, width, LANE_WIDTH, B, L, merge_pts, line_pos):
        super().__init__(width, B*LANE_WIDTH, False)
        self.LANE_WIDTH = LANE_WIDTH
        self.B = B
        self.line_pos = line_pos
        self.merge_pts = merge_pts

class Booth(Agent):
    """Spawns vehicles according to control algorithms"""
    def __init__(self, lane, model):
        super().__init__(lane, model)
        self.count = 0
        #self.y = (lane-1/2)*self.model.map.LANE_WIDTH
        self.vel = 0
        
    def open_gate(self):
        lane = self.unique_id
        v = Vehicle(lane*1000+self.count, self.model, self.vel, 2*(lane-1))
        self.model.schedule.add(v)
        #self.model.map.place_agent(v, (0,self.y))
        self.model.map.place_agent(v, (0,self.pos[1]))
        self.count += 1
        
    def get_y(self):
        return self.y
        
    def get_vel(self):
        return self.vel
        

class Vehicle(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, vel, line):
        super().__init__(unique_id, model)
        #physical attributes
        self.id = unique_id
        self.width = 6 #feet
        self.length = 15 # feet
        self.max_speed = 30*1.46667 #feet/sec
        self.accel = 10*1.46667
        self.decel = 10*1.46667
        self.merge_vel = 5*1.46667
        
        #state attributes
        self.line = line
        self.goal = line
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
        
    def get_new_goal(self):
        arr = self.model.map.merge_pts
        merge_left = self.line == 0 or 0 < arr[self.line-1] < arr[self.line]
        self.goal = self.line+2*merge_left-1
        #print(self.goal)
        
    def merge(self):
        #print(self.goal)
        if self.merging:
            print(self.line,self.goal)
            y = self.pos[1]
            arr = self.model.map.line_pos
            if abs(y-arr[self.goal]) <= 0.5:
                self.line = self.goal
                self.y_vel = 0
                self.merging = False
        else:
            direction = 2*(self.line < self.goal)-1
            self.y_vel = direction*self.merge_vel
            self.merging = True
    
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
        blocked = False
        #if path ahead blocked
        for car in self.model.schedule.agents:
            if isinstance(car,Vehicle) and car.unique_id != self.unique_id:
                if car.line == self.line or \
                    (self.merging and car.line == self.goal) or \
                    (car.merging and car.goal == self.line):
                        if 0 < (car.pos[0] - x - car.length + car.x_vel*stop_time) \
                        <= stop_dist + 1:
                            blocked = True
                            break
        if blocked:
            self.brake()
        #if current lane will end
        elif 0 < self.model.map.merge_pts[self.line] <= x + stop_dist + 1:
            self.get_new_goal() #update goal
            #if safe, merge
            if True:
                self.merge()
            #else, brake
            else:
                self.brake()
        #else space ahead is free
        else:
            #accelerate/maintain speed
            self.accelerate()
        self.move()
        #print('Vehicle ',self.unique_id,' is @', x,' ft.')

class TollBoothModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, LANE_WIDTH, B, L, merge_pts, line_pos, dt):
        self.dt = dt
        self.time = 0
        self.map = Map(width,LANE_WIDTH,B,L,merge_pts,line_pos)
        self.schedule = BaseScheduler(self)
        
        # Create booths
        for i in range(1,B+1):
            b = Booth(i, self)
            self.schedule.add(b)
            self.map.place_agent(b, (0,(i-1/2)*LANE_WIDTH))
        
        self.datacollector = DataCollector(
            model_reporters={},
            agent_reporters={"Position": lambda v: v.pos})

    def step(self):
        '''Advance the model by one step.'''
        # TollBooth Control Algorithm
        for agent in self.schedule.agents:
            if isinstance(agent,Booth):
                if agent.unique_id == 1 and self.schedule.steps % 80 == 0:
                    agent.open_gate()
                elif agent.unique_id == 2 and self.schedule.steps % 80 == 0:
                    agent.open_gate()
                    
        #for agent in self.schedule.agents:
        #    if isinstance(agent,Vehicle):
        #        
                    
        self.datacollector.collect(self)        
        self.schedule.step()
        self.time += self.dt
        #print(round(self.time,2))

