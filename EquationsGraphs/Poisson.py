import matplotlib.pyplot as plt
import random as rand
import math

lamb = 0.4
k = 1
t = 15

def myPlot(x, y, name):
    plt.plot(x, y, linewidth=1.0, label=name)
    plt.legend(loc="upper left")
    plt.grid(linewidth = 0.5)

def possion_kt(lamb, k, t):
    poisson = (math.pow((lamb * t), k) / math.factorial(k)) * math.pow(math.e, -(lamb * t))
    return poisson

def PDF(lamb, t):
    pdf = lamb * math.pow(math.e, -(lamb * t))
    return pdf

def CPF(lamb, t):
    cpf = 1 - math.pow(math.e, -(lamb * t))
    return cpf

def integral(lamb, k, t):
    area = 0
    for i in range(t+1):
        area += possion_kt(lamb, k, i+1)
    return area

x = []
y_possion = []
y_pdf = []
y_cpf = []
for i in range(t):
    x.append(i)
    y_possion.append(possion_kt(lamb, k, i))
    y_pdf.append(PDF(lamb, i))
    y_cpf.append(CPF(lamb, i))

myPlot(x, y_possion, "possion")
myPlot(x, y_pdf, "pdf")
myPlot(x, y_cpf, "cdf")

plt.show()



