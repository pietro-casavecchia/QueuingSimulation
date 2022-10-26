
import matplotlib.pyplot as plt
import math

Lambda = 5
Mu = 50.0

def myPlot(x, y, name):
    plt.plot(x, y, linewidth=1.0, label=name)
    plt.legend(loc="upper left")
    plt.grid(linewidth = 0.5)
    

def possion(Lambda, x):
    poisson = (math.pow(Lambda, x) * math.pow(math.e, -Lambda)) / float(math.factorial(x))
    return poisson

def exponential(Mu, x):
    exponential = Lambda * math.pow(math.e, -(Lambda * x))
    return exponential

x = []
y_p = []
y_e = []
for i in range(90):
    x.append(i)
    y_p.append(possion(Lambda, i))
    y_e.append(exponential(Mu, i))

myPlot(x, y_e, "Exp")
plt.show()