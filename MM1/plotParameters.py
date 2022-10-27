import matplotlib.pyplot as plt
import math

S = 2
max_IA = 10
interval = 1

array_Plot_Rho = []
array_Plot_Ls = []
array_Plot_Lq = []
array_Plot_Ws = []
array_Plot_Wq = []

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
    Plot_Lambda = round((1 / IA), 3)
    Plot_Mu = round((1 / S), 3)
    Plot_Rho = round((Plot_Lambda / Plot_Mu), 3)

    Plot_Ls = round((Plot_Rho / (1 - Plot_Rho)), 3)
    Plot_Lq = round((Plot_Lambda**2 / (Plot_Mu * (Plot_Mu - Plot_Lambda))), 3)
    Plot_Ws = round((1 / (Plot_Mu - Plot_Lambda)), 3) 
    Plot_Wq = round((Plot_Lambda / (Plot_Mu * (Plot_Mu - Plot_Lambda))), 3) 

    array_Plot_Rho.append(Plot_Rho)
    array_Plot_Ls.append(Plot_Ls)
    array_Plot_Lq.append(Plot_Lq)
    array_Plot_Ws.append(Plot_Ws)
    array_Plot_Wq.append(Plot_Wq)

multiPlotLog(
    array_Plot_Rho, 
    array_Plot_Ls, 
    array_Plot_Lq, 
    array_Plot_Ws, 
    array_Plot_Wq, 
    "Ls", "Lq", "Ws", "Wq")

multiPlotScale(
    array_Plot_Rho, 
    array_Plot_Ls, 
    array_Plot_Lq, 
    array_Plot_Ws, 
    array_Plot_Wq, 
    "Ls", "Lq", "Ws", "Wq")
    



