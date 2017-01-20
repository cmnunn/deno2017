# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:52:42 2017

@author: cmnunn
"""
from MoneyModel import MoneyModel
import matplotlib.pyplot as plt

model = MoneyModel(50, 10, 10)
for i in range(100):
    model.step()
    
gini = model.datacollector.get_model_vars_dataframe()
gini.plot()

agent_wealth = model.datacollector.get_agent_vars_dataframe()
agent_wealth.head()