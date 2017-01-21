# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:11:55 2017

@author: cmnunn
"""
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
#from mesa.datacollection import DataCollector
#import random
#import numpy as np

class Map(ContinuousSpace):
    """Space of the toll plaza, with defined lanes & bounds"""
    def __init__(self, width, LANE_WIDTH, LANE_SPACING, B, L, merge_pts):
        super().__init__(width, B*LANE_WIDTH+(B-1)*LANE_SPACING, False)
        self.LANE_WIDTH = LANE_WIDTH
        self.LANE_SPACING = LANE_SPACING
        self.B = B
        self.merge_pts = merge_pts

class Booth(Agent):
    """Spawns vehicles according to control algorithms"""
    def __init__(self, lane, model):
        super().__init__(lane, model)
        self.count = 0
        self.y = lane*self.model.map.LANE_WIDTH/2 + \
                (lane-1)*self.model.map.LANE_SPACING
        self.vel = 0
        
    def open_gate(self):
        v = Vehicle(self.lane*1000+self.count, self.model, self.vel, self.lane)
        self.model.schedule.add(v)
        self.model.map.place_agent(v, (0,self.y))
        self.count += 1
        
    def get_y(self):
        return self.y
        
    def get_vel(self):
        return self.vel
        

class Vehicle(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, vel, lane):
        super().__init__(unique_id, model)
        self.id = unique_id
        self.lane = lane
        self.width = 8 #feet
        self.length = 15 # feet
        self.x_vel = vel
        self.y_vel = 0
        self.max_speed = 30*1.46667 #feet/sec
        
    def brake(self):
        #decrease velocity
        self.x_vel = 0
        
    def accel(self):
        #increase velocity
        self.x_vel = self.max_speed
        
    def get_merge_direction(self):
        '''returns True if the next lane to merge to is left (False if Right)'''
        x = self.pos[0]
        roads = self.model.map
        arr = roads.merge_pts
        return(self.lane < roads.B and \
                (arr[2*int(self.lane)] == 0 or arr[2*int(self.lane)] > x))
        
    def merge(self):
        pass
    
    def move(self):
        dt = self.model.dt
        x = self.pos[0], y = self.pos[1]
        self.model.map.move_agent(self, (x+dt*self.x_vel,y+dt*self.y_vel))
    
    def step(self):
        #check if lane has ended
        x = self.pos[0]
        arr = self.model.map.merge_pts
        if 0 < x <= arr[2*int(self.lane-1)]:
            if self.x_vel > 0:
                self.brake()
            else:
                self.merge()
        else:
            self.accel()
        self.move()

class TollBoothModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, LANE_WIDTH, LANE_SPACING, B, L, merge_pts, dt):
        self.dt = dt
        self.time = 0
        self.map = Map(width,LANE_WIDTH,LANE_SPACING,B,L,merge_pts)
        self.schedule = BaseScheduler(self)
        
        # Create booths
        for i in range(1,B+1):
            b = Booth(i, self)
            self.schedule.add(b)
            
        # Remove out-of-bounds vehicles
        for agent in self.schedule.agents[:]:
            if agent.unique_id > B:
                if self.map.out_of_bounds(agent.pos):
                    self.schedule.remove(agent)
        
        #self.datacollector = DataCollector(
        #    model_reporters={"Gini": compute_gini},
        #    agent_reporters={"Wealth": lambda a: a.wealth})

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)        
        self.schedule.step()
        self.time += self.dt

