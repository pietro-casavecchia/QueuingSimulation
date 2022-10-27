import matplotlib.pyplot as plt
import math

S = 5
max_IA = 50
interval = 0.1

array_Rho = []
array_Ls = []
array_Lq = []
array_Ws = []
array_Wq = []

def multiPlotLog(x, y_1, y_2, y_3, y_4, name_1, name_2, name_3, name_4):
    figure, axis = plt.subplots(2, figsize=(5, 7))
    axis[0].plot(x, y_1, linewidth=1.0, label=name_1)
    axis[0].plot(x, y_2, linewidth=1.0, label=name_2)
    axis[0].set_yscale('log')
    axis[0].grid(linewidth = 0.5)
    axis[0].legend(loc="upper left")
    axis[1].plot(x, y_3, linewidth=1.0, label=name_3)
    axis[1].plot(x, y_4, linewidth=1.0, label=name_4)
    axis[1].set_yscale('log')
    axis[1].grid(linewidth = 0.5)
    axis[1].legend(loc="upper left")
    plt.show()

def multiPlotScale(x, y_1, y_2, y_3, y_4, name_1, name_2, name_3, name_4):
    figure, axis = plt.subplots(2, figsize=(5, 7))
    axis[0].plot(x, y_1, linewidth=1.0, label=name_1)
    axis[0].plot(x, y_2, linewidth=1.0, label=name_2)
    axis[0].grid(linewidth = 0.5)
    axis[0].legend(loc="upper left")
    axis[1].plot(x, y_3, linewidth=1.0, label=name_3)
    axis[1].plot(x, y_4, linewidth=1.0, label=name_4)
    axis[1].grid(linewidth = 0.5)
    axis[1].legend(loc="upper left")
    plt.show()

steps = math.floor((max_IA - S) / interval)

IA = max_IA
for i in range(steps - 1):
    IA -= interval
    Lambda = round((1 / IA), 3)
    Mu = round((1 / S), 3)
    Rho = round((Lambda / Mu), 3)

    Ls = round((Rho / (1 - Rho)), 3)
    Lq = round((Lambda**2 / (Mu * (Mu - Lambda))), 3)
    Ws = round((1 / (Mu - Lambda)), 3) 
    Wq = round((Lambda / (Mu * (Mu - Lambda))), 3) 

    array_Rho.append(Rho)
    array_Ls.append(Ls)
    array_Lq.append(Lq)
    array_Ws.append(Ws)
    array_Wq.append(Wq)

multiPlotLog(
    array_Rho, 
    array_Ls, 
    array_Lq, 
    array_Ws, 
    array_Wq, 
    "Ls", "Lq", "Ws", "Wq",)

multiPlotScale(
    array_Rho, 
    array_Ls, 
    array_Lq, 
    array_Ws, 
    array_Wq, 
    "Ls", "Lq", "Ws", "Wq",)
    



