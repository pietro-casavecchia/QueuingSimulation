from turtle import pos
import matplotlib.pyplot as plt
import random as rand
import math

lamb = 0.12
k = 3

def myPlot(x, y):
    plt.plot(x, y, color=(0, 0, 0), linewidth=1.0)
    plt.grid(linewidth = 0.5)
    

def possion_kt(lamb, k, t):
    poisson = (math.pow((lamb * t), k) / math.factorial(k)) * math.pow(math.e, -(lamb * t))
    return poisson
'''
x = []
y = []
for i in range(100):
    x.append(i)
    y.append(possion_kt(lamb, k, i))
'''

def makeP(lamb, k):
    x = []
    y = []
    for i in range(100):
        x.append(i)
        y.append(possion_kt(lamb, k, i))
    return x, y

for i in range(50):
    x, y = makeP(lamb, i)
    myPlot(x, y)

#myPlot(x, y)

plt.show()