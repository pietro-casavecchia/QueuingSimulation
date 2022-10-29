import matplotlib.pyplot as plt
import random as rand
import math

labda = 0.4

def poisson_arrival(labda, interArrival_time):
    generated = False
    # PDF of tau equal to time 
    PDF = round(labda * math.pow(math.e, -(labda * interArrival_time)), 2)
    # simulate probabiliy 
    throw = rand.randint(0, 100) / 100
    # test if throw <= then PDF then pkg is generated 
    if throw <= PDF:
        generated = True
    return generated 

for i in range(10):
    print(i, poisson_arrival(labda, i))



