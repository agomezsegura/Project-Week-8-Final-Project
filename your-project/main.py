#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import pickle
from matplotlib import style
import time

style.use("ggplot")


# In[2]:


class TrafficLights:
    def __init__(self, env):
        self.x1 = 33 // env.m
        self.y1 = 33 % env.n
        self.c1 = 'red'
        self.x2 = 36 // env.m
        self.y2 = 36 % env.n
        self.c2 = 'green'
        self.x3 = 63 // env.m
        self.y3 = 63 % env.n
        self.c3 = 'green'
        self.x4 = 66 // env.m
        self.y4 = 66 % env.n
        self.c4 = 'red'

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)

    def action(self, choice):
        '''
        Gives us 2 options.
        '''
        if choice == 'C':
            self.change('C')
            
    def change(self, action = False):
        if not action:
            choice_pair1 = random.choice(['green', 'red'])
            choice_pair2 = random.choice(['green', 'red'])
            self.c1 = choice_pair1
            self.c2 = choice_pair2
            self.c3 = choice_pair2
            self.c4 = choice_pair1
        else:
            if action == 'C':
                if self.c1 == 'green':
                    self.c1 = 'red'
                else:
                    self.c1 = 'green'
                if self.c2 == 'green':
                    self.c2 = 'red'
                else:
                    self.c2 = 'green'
                if self.c3 == 'green':
                    self.c3 = 'red'
                else:
                    self.c3 = 'green'
                if self.c4 == 'green':
                    self.c4 = 'red'
                else:
                    self.c4 = 'green'


# In[3]:


class Car:
    def __init__(self, pos, flow, env):
        self.x = pos // env.m
        self.y = pos % env.n
        self.flow = flow
    def move(self):
        if self.flow == 'H-R':
            self.y += 1
        elif self.flow == 'H-L':
            self.y -= 1
        elif self.flow == 'V-U':
            self.x -= 1
        elif self.flow == 'V-D':
            self.x += 1


# In[ ]:


class GridWorld(object):
    def __init__(self, m, n):
        self.grid = np.zeros((m,n,3), dtype = np.uint8)
        self.m = m
        self.n = n
        self.colors = {'red': (0, 0, 255),
                       'blue': (255, 0, 0),
                       'green': (0, 255, 0),
                       'yellow': (0, 255, 255),
                       'grey': (105, 105, 105)
                      }
        self.actionSpace = {'K': 'same colors', 'C': 'change colors'}
        self.possibleActions = ['K', 'C']
        self.Buildings = [0, 1, 2, 3, 6, 7, 8, 9,
                          10, 11, 12, 13, 16, 17, 18, 19,
                          20, 21, 22, 23, 26, 27, 28, 29,
                          30, 31, 32, 33, 36, 37, 38, 39,
                          60, 61, 62, 63, 66, 67, 68, 69,
                          70, 71, 72, 73, 76, 77, 78, 79,
                          80, 81, 82, 83, 86, 87, 88, 89,
                          90, 91, 92, 93, 96, 97, 98, 99]
        self.addTrafficLights(self)
        self.addCars(self)

    def addBuildings(self):
        for building in self.Buildings:
            x = building // self.m
            y = building % self.n
            self.grid[x][y] = self.colors['grey']
    
    def addTrafficLights(self, env):
        self.TrafficLights = TrafficLights(env)
        env.grid[env.TrafficLights.x1][env.TrafficLights.y1] = env.colors[env.TrafficLights.c1]
        env.grid[env.TrafficLights.x2][env.TrafficLights.y2] = env.colors[env.TrafficLights.c2]
        env.grid[env.TrafficLights.x3][env.TrafficLights.y3] = env.colors[env.TrafficLights.c3]
        env.grid[env.TrafficLights.x4][env.TrafficLights.y4] = env.colors[env.TrafficLights.c4]
    
    def addCars(self, env):
        car1 = Car(4, 'V-D', env)
        car2 = Car(95, 'V-U', env)
        car3 = Car(50, 'H-R', env)
        car4 = Car(49, 'H-L', env)
        cars = []
        cars.append(car1)
        cars.append(car2)
        cars.append(car3)
        cars.append(car4)
        self.Cars = cars
        for car in self.Cars:
            self.grid[car.x][car.y] = self.colors['yellow']

    def update_grid(self):
        self.grid = np.zeros((self.m, self.n, 3), dtype = np.uint8)
        self.addBuildings()
        self.grid[self.TrafficLights.x1][self.TrafficLights.y1] = self.colors[self.TrafficLights.c1]
        self.grid[self.TrafficLights.x2][self.TrafficLights.y2] = self.colors[self.TrafficLights.c2]
        self.grid[self.TrafficLights.x3][self.TrafficLights.y3] = self.colors[self.TrafficLights.c3]
        self.grid[self.TrafficLights.x4][self.TrafficLights.y4] = self.colors[self.TrafficLights.c4]
#         for car in self.Cars:
#             car.move()
#             self.grid[car.x][car.y] = self.colors['yellow']
        return self.grid
            
    def render(self):
        self.grid = self.update_grid()
        img = Image.fromarray(self.grid, 'RGB')
        img = img.resize((300, 300))
        cv2.imshow("image", np.array(img))
            

n_episodes = 25000
show_every = 1000
for episode in range(n_episodes):
    env = GridWorld(10, 10)
    if episode % show_every == 0:
        print(f"on #{episode}")
        show = True
    else:
        show = False
        
    for i in range(200):
        if show:
            env.grid = np.zeros((env.m, env.n, 3), dtype = np.uint8)
            env.addBuildings()
            env.grid[env.TrafficLights.x1][env.TrafficLights.y1] = env.colors[env.TrafficLights.c1]
            env.grid[env.TrafficLights.x2][env.TrafficLights.y2] = env.colors[env.TrafficLights.c2]
            env.grid[env.TrafficLights.x3][env.TrafficLights.y3] = env.colors[env.TrafficLights.c3]
            env.grid[env.TrafficLights.x4][env.TrafficLights.y4] = env.colors[env.TrafficLights.c4]
            img = Image.fromarray(env.grid, 'RGB')
            img = img.resize((300, 300))
            cv2.imshow("image", np.array(img))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


# ---
