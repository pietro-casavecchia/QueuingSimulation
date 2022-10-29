
'''
No zero
Loop Rho
Quadri plot
need to wait one for the server
'''

import matplotlib.pyplot as plt
import numpy as np
import math

# costant serving variable
S = 5
max_IA = 25
interval = 0.5

# system variables 
print_dataframe = False
print_graphs = False
simulation_time = 40000
n_experiments = 3

class Package:
    def __init__(self):
        self.id_number = None

class Buffer:
    def __init__(self):
        self.queue = []
    
    def calculate_buffer_size(self):
        return len(self.queue)

class Server:
    def __init__(self):
        self.pkg_serving = None
        self.status = 0
        self.serving_time = None
        self.service_progression = None

        # parameters and feedback
        self.array_serving_time = []
    
    def from_buffer_to_server(self, buffer):
        # FIFO buffer
        # get first pkg
        pkg = buffer.queue[0]
        # eliminate from queue
        buffer.queue.pop(0)
        # move into the server change server status
        self.status = 1
        self.pkg_serving = pkg

        # generate a serving time > 0
        while True:
            self.serving_time = math.floor(np.random.exponential(S))
            # self.serving_time = np.random.poisson(S)
            if self.serving_time > 0:
                break
        # initiate service progression 
        self.service_progression = 0

        # append serving time for feedback 
        self.array_serving_time.append(self.serving_time)
    
    def service(self, buffer, pkgs_served):
        # if status of the server is zero and a pkg in the buffer exits then move the pkg into the server
        if self.status == 0 and buffer.calculate_buffer_size() == 0:
            # erase pkg given exited the server 
            self.pkg_serving = None
            # empty the server 
            self.serving_time = None
            self.service_progression = None
        elif self.status == 0 and buffer.calculate_buffer_size() > 0:
            self.from_buffer_to_server(buffer)
    
        # if the serving time == 0 then after the from_buffer...() call the status will be 1 
        if self.status == 1:
            self.service_progression += 1
            if self.service_progression > self.serving_time:
                # append in pkgs served
                pkgs_served.append(self.pkg_serving)

                self.status = 0

class System():
    def __init__(self, run_time, IA):
        self.IA = IA
        self.run_time = run_time
        self.current_time = 0
        self.n_pkgs = 0
        self.pkgs_served = []

        # generation of pkg variabiles
        self.inter_arrival_time = None
        self.generation_progression = None

        # generate a buffer and server
        self.buffer = Buffer()
        self.server = Server()

        # parameters and feedback
        # number of pkgs nel sistema for every unit of time 
        self.array_inter_arrival_time = []
        self.pkgs_sys_for_unitTime = []
        self.pkgs_queue_for_unitTime = []
        self.dict_pkgsTime_queue = {}
        self.dict_pkgsTime_system = {}
        # array counter for how many pkgs in the system [a, b]
        # a: how many time there are none and b: how many time there > 0
        self.array_P01 = [0, 0]

        # start simulation call
        self.simulation()

    def pkg_generation(self):
        # initialize pkg to none 
        pkg = None
        # run the generation only for the run time time 
        if self.current_time < self.run_time:
            # generate pkg zero
            if (
                (self.current_time == 0) or 
                (self.generation_progression >= self.inter_arrival_time)
                ):
                pkg = Package()
                pkg.id_number = self.n_pkgs
                self.n_pkgs += 1
                # inter arrival time > 0
                while True:
                    self.inter_arrival_time = math.floor(np.random.exponential(self.IA))
                    # self.inter_arrival_time = np.random.poisson(self.IA)
                    if self.inter_arrival_time > 0:
                        break
                # set generation progression to zero for initialize it 
                self.generation_progression = 0

                # append gen time for feedback 
                self.array_inter_arrival_time.append(self.inter_arrival_time)
            
            # increment only if self.inter_arrival_time != 0 because the pkg gen fn will be called again
            if self.inter_arrival_time != 0:
                self.generation_progression += 1
        else: 
            self.inter_arrival_time = None
            self.generation_progression = None
        
        return pkg 
        
    def simulation(self): 
        # continue the process until all pks are served 
        while (self.current_time < self.run_time):

            # --- --- --- start sys call --- --- --- 

            # menage generation 
            pkg = self.pkg_generation()
            # manage buffer 
            if pkg != None: self.buffer.queue.append(pkg)
            # manage server
            self.server.service(self.buffer, self.pkgs_served)

            # --- --- --- end sys call --- --- --- 

            # --- --- --- start feedback --- --- ---
            # Ls Lq
            self.pkgs_sys_for_unitTime.append(self.n_pkgs - len(self.pkgs_served))
            self.pkgs_queue_for_unitTime.append(self.n_pkgs - len(self.pkgs_served) - self.server.status)
            # calculate how long a pkg in the queue
            for i in range(len(self.buffer.queue)):
                # get value of  pkg 
                value_queue_pkg = self.dict_pkgsTime_queue.get(self.buffer.queue[i].id_number)
                # if is none set to 1 else increment by 1 
                if value_queue_pkg == None:
                    self.dict_pkgsTime_queue.update({self.buffer.queue[i].id_number: 1})
                else:
                    self.dict_pkgsTime_queue.update({self.buffer.queue[i].id_number: value_queue_pkg + 1})
            # calculate how long a pkg in the server 
            # read the value in the server 
            #   check if already exits in the dict then add 1 else increase by one 
            if self.server.pkg_serving != None:
                # search it in the 
                value_server_pkg = self.dict_pkgsTime_system.get(self.server.pkg_serving.id_number)
                if value_server_pkg == None:
                    self.dict_pkgsTime_system.update({self.server.pkg_serving.id_number: 1})
                else:
                    self.dict_pkgsTime_system.update({self.server.pkg_serving.id_number: value_server_pkg + 1})
            # calculate value probability 0 add it to array first index is when queue
            if len(self.buffer.queue) == 0 and self.server.status == 0:
                self.array_P01[0] += 1
            else:
                self.array_P01[1] += 1
            # --- --- --- end feedback --- --- ---
            
            print(self.n_pkgs, end="\r")

            # increment simulation time 
            self.current_time += 1
        

    def calculate_parameters(self):
        # take the value from the dict of waiting time in the server / queue
        array_waitingTime_queue = []
        array_waitingTime_server = []
        for values_q in self.dict_pkgsTime_queue.values():
            array_waitingTime_queue.append(values_q)
        # adjust with adding 1 for mean for missing pks 
        for _ in range(self.n_pkgs - len(array_waitingTime_queue)):
            array_waitingTime_queue.append(0)

        for values_s in self.dict_pkgsTime_system.values():
            array_waitingTime_server.append(values_s)
        # adjust with adding 1 for mean for missing pks 
        for _ in range(self.n_pkgs - len(array_waitingTime_server)):
            array_waitingTime_server.append(0)


        return (
            self.array_inter_arrival_time,
            self.server.array_serving_time,
            self.pkgs_sys_for_unitTime,  
            self.pkgs_queue_for_unitTime,
            array_waitingTime_server,
            array_waitingTime_queue,
            self.array_P01
            )

# array for multiple rho 
n_Rho = []
Ls_fnRho = []
Lq_fnRho = []
Ws_fnRho = []
Wq_fnRho = []
# array for multiple experiments
experiment_no = []
# variable for avg of every exp 
array_IA = []
array_S = []
array_Lambda = []
array_Mu = []
array_Rho = []
array_Ls = []
array_Lq = []
array_Ws = []
array_Wq = []
array_P0 = []

steps = math.floor((max_IA - S) / interval)
IA = max_IA
for r in range(steps - 1):
    np.random.seed(42)

    IA -= interval
    n_Rho.append(round((S / IA), 3))

    for i in range(n_experiments):
        # unit time for plot 
        experiment_no.append(i)

        (   array_inter_arrival_time,
            array_serving_time,
            pkgs_sys_for_unitTime, 
            pkgs_queue_for_unitTime,
            array_waitingTime_server,
            array_waitingTime_queue,
            array_P01
            ) = System(simulation_time, IA).calculate_parameters()

        # calculate exp values
        avg_interArrival = np.mean(array_inter_arrival_time)
        avg_serving = np.mean(array_serving_time)
        Lambda = 1 / avg_interArrival
        Mu = 1 / avg_serving
        Rho = Lambda / Mu
        if len(pkgs_sys_for_unitTime) == 0:
            Ls = 0
        else:
            Ls = np.mean(pkgs_sys_for_unitTime)
        if len(pkgs_queue_for_unitTime) == 0:
            Lq = 0
        else:
            Lq = np.mean(pkgs_queue_for_unitTime)
        if len(array_waitingTime_queue) == 0:
            Wq = 0
        else:
            Wq = np.mean(array_waitingTime_queue)
        Ws = Wq + np.mean(array_waitingTime_server)
        P0 = array_P01[0] / (array_P01[0] + array_P01[1])

        # append for avg exp 
        array_IA.append(avg_interArrival)
        array_S.append(avg_serving)
        array_Lambda.append(Lambda)
        array_Mu.append(Mu)
        array_Rho.append(Rho)
        array_Ls.append(Ls)
        array_Lq.append(Lq)
        array_Ws.append(Ws)
        array_Wq.append(Wq)
        array_P0.append(P0)

        # calculate theo values 
        Lambda_theo = 1 / IA
        Mu_theo = 1 / S
        Rho_theo = Lambda_theo / Mu_theo
        Ls_theo = Rho_theo / (1 - Rho_theo)
        Lq_theo = (Lambda_theo**2) / (Mu_theo * (Mu_theo - Lambda_theo))
        Ws_theo = 1 / (Mu_theo - Lambda_theo)
        Wq_theo = Lambda_theo / (Mu_theo * (Mu_theo - Lambda_theo))
        P0_theo = 1 - Rho_theo

        # prints of hist and Ls of 1 experiment
        if print_graphs == True:

            '''plt.hist(array_serving_time, bins=30) 
            plt.hist(array_inter_arrival_time, bins=30) 
            plt.show() '''

            ut = []
            for i in range(len(pkgs_sys_for_unitTime)):
                ut.append(i)

            plt.plot(ut, pkgs_sys_for_unitTime, color=(0, 0, 0), linewidth=1.0)
            plt.grid(linewidth = 0.5)
            plt.show()

    # --- --- --- out avg result for n experiment --- --- ---

    out_IA = round(np.mean(array_IA), 3)
    out_S = round(np.mean(array_S), 3)
    out_Lambda = round(np.mean(array_Lambda), 3)
    out_Mu = round(np.mean(array_Mu), 3)
    out_Rho = round(np.mean(array_Rho), 3)
    out_Ls = round(np.mean(array_Ls), 3) 
    out_Lq = round(np.mean(array_Lq), 3) 
    out_Ws = round(np.mean(array_Ws), 3) 
    out_Wq = round(np.mean(array_Wq), 3) 
    out_P0 = round(np.mean(array_P0), 3) 

    # append for graph in fn of Rho 
    Ls_fnRho.append(out_Ls)
    Lq_fnRho.append(out_Lq)
    Ws_fnRho.append(out_Ws)
    Wq_fnRho.append(out_Wq)

    # calculate percentage error 
    error_IA = math.floor(-(IA - out_IA) / IA * 100)
    error_S = math.floor(-(S - out_S) / S * 100)
    error_Lambda = math.floor(-(Lambda_theo - out_Lambda) / Lambda_theo * 100)
    error_Mu = math.floor(-(Mu_theo - out_Mu) / Mu_theo * 100)
    error_Rho = math.floor(-(Rho_theo - out_Rho) / Rho_theo * 100)
    error_Ls = math.floor(-(Ls_theo - out_Ls) / Ls_theo * 100)
    error_Lq = math.floor(-(Lq_theo - out_Lq) / Lq_theo * 100)
    error_Ws = math.floor(-(Ws_theo - out_Ws) / Ws_theo * 100)
    error_Wq = math.floor(-(Wq_theo - out_Wq) / Wq_theo * 100)
    error_P0 = math.floor(-(P0_theo - out_P0) / P0_theo * 100)

    print("IA theo: {} IA out: {} error: {}".format(IA, out_IA, error_IA))
    print("S theo: {} S out: {} error: {}".format(S, out_S, error_S))
    print("Lambda theo: {} Lambda out: {} error: {}".format(round(Lambda_theo, 3), out_Lambda, error_Lambda))
    print("Mu theo: {} Mu out: {} error: {}".format(round(Mu_theo, 3), out_Mu, error_Mu))
    print("Rho theo: {} Rho out: {} error: {}".format(round(Rho_theo, 3), out_Rho, error_Rho))
    print("Ls theo: {} Ls out: {} error: {}".format(round(Ls_theo, 3), out_Ls, error_Ls))
    print("Lq theo: {} Lq out: {} error: {}".format(round(Lq_theo, 3), out_Lq, error_Lq))
    print("Ws theo: {} Ws out: {} error: {}".format(round(Ws_theo, 3), out_Ws, error_Ws))
    print("Wq theo: {} Wq out: {} error: {}".format(round(Wq_theo, 3), out_Wq, error_Wq))
    print("P0 theo: {} P0 out: {} error: {}".format(round(P0_theo, 3), out_P0, error_P0))


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

multiPlotLog(
    n_Rho, 
    Ls_fnRho, 
    Lq_fnRho, 
    Ws_fnRho, 
    Wq_fnRho, 
    "Ls", "Lq", "Ws", "Wq")


# Theo with Experiemnt plot
# Theo calculation 
array_Plot_Rho = []
array_Plot_Ls = []
array_Plot_Lq = []
array_Plot_Ws = []
array_Plot_Wq = []
# Reset to starting value IA
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

def LPlotLog(
    x, 
    Ls, Ls_e,
    Lq, Lq_e,
    name_Ls, name_Ls_e,
    name_Lq, name_Lq_e):
    figure, axis = plt.subplots(2, figsize=(4, 7))
    # Ls
    axis[0].plot(x, Ls, linewidth=1.0, color=(0, 0, 0), label=name_Ls)
    axis[0].plot(x, Ls_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Ls_e)
    axis[0].set_yscale('log')
    axis[0].grid(linewidth = 0.5)
    axis[0].legend(loc="best")
    # Lq
    axis[1].plot(x, Lq, linewidth=1.0, color=(0, 0, 0), label=name_Lq)
    axis[1].plot(x, Lq_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Lq_e)
    axis[1].set_yscale('log')
    axis[1].grid(linewidth = 0.5)
    axis[1].legend(loc="best")

    plt.show()

LPlotLog(
    n_Rho, 
    array_Plot_Ls, Ls_fnRho,
    array_Plot_Lq, Lq_fnRho, 
    "Ls", "Ls exp",
    "Lq", "Lq exp")

def LPlot(
    x, 
    Ls, Ls_e,
    Lq, Lq_e,
    name_Ls, name_Ls_e,
    name_Lq, name_Lq_e):
    figure, axis = plt.subplots(2, figsize=(4, 7))
    # Ls
    axis[0].plot(x, Ls, linewidth=1.0, color=(0, 0, 0), label=name_Ls)
    axis[0].plot(x, Ls_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Ls_e)
    axis[0].grid(linewidth = 0.5)
    axis[0].legend(loc="best")
    # Lq
    axis[1].plot(x, Lq, linewidth=1.0, color=(0, 0, 0), label=name_Lq)
    axis[1].plot(x, Lq_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Lq_e)
    axis[1].grid(linewidth = 0.5)
    axis[1].legend(loc="best")

    plt.show()

LPlot(
    n_Rho, 
    array_Plot_Ls, Ls_fnRho,
    array_Plot_Lq, Lq_fnRho, 
    "Ls", "Ls exp",
    "Lq", "Lq exp")

def WPlotLog(
    x, 
    Ws, Ws_e,
    Wq, Wq_e,
    name_Ws, name_Ws_e,
    name_Wq, name_Wq_e):
    figure, axis = plt.subplots(2, figsize=(4, 7))
    # Ws
    axis[0].plot(x, Ws, linewidth=1.0, color=(0, 0, 0), label=name_Ws)
    axis[0].plot(x, Ws_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Ws_e)
    axis[0].set_yscale('log')
    axis[0].grid(linewidth = 0.5)
    axis[0].legend(loc="best")
    # Wq
    axis[1].plot(x, Wq, linewidth=1.0, color=(0, 0, 0), label=name_Wq)
    axis[1].plot(x, Wq_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Wq_e)
    axis[1].set_yscale('log')
    axis[1].grid(linewidth = 0.5)
    axis[1].legend(loc="best")

    plt.show()

WPlotLog(
    n_Rho, 
    array_Plot_Ws, Ws_fnRho, 
    array_Plot_Wq, Wq_fnRho, 
    "Ws", "Ws exp",
    "Wq", "Wq exp")

def WPlot(
    x, 
    Ws, Ws_e,
    Wq, Wq_e,
    name_Ws, name_Ws_e,
    name_Wq, name_Wq_e):
    figure, axis = plt.subplots(2, figsize=(4, 7))
    # Ws
    axis[0].plot(x, Ws, linewidth=1.0, color=(0, 0, 0), label=name_Ws)
    axis[0].plot(x, Ws_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Ws_e)
    axis[0].grid(linewidth = 0.5)
    axis[0].legend(loc="best")
    # Wq
    axis[1].plot(x, Wq, linewidth=1.0, color=(0, 0, 0), label=name_Wq)
    axis[1].plot(x, Wq_e, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label=name_Wq_e)
    axis[1].grid(linewidth = 0.5)
    axis[1].legend(loc="best")

    plt.show()

WPlot(
    n_Rho, 
    array_Plot_Ws, Ws_fnRho, 
    array_Plot_Wq, Wq_fnRho, 
    "Ws", "Ws exp",
    "Wq", "Wq exp")






'''def quardiPlotLog(
    x, 
    Ls, Ls_e,
    Lq, Lq_e,
    Ws, Ws_e,
    Wq, Wq_e,
    name_Ls, name_Ls_e,
    name_Lq, name_Lq_e,
    name_Ws, name_Ws_e,
    name_Wq, name_Wq_e):
    figure, axis = plt.subplots(2, 2, figsize=(8, 7))
    # Ls
    axis[0, 0].plot(x, Ls, linewidth=1.0, label=name_Ls)
    axis[0, 0].plot(x, Ls_e, linewidth=1.0, label=name_Ls_e)
    axis[0, 0].set_yscale('log')
    axis[0, 0].grid(linewidth = 0.5)
    axis[0, 0].legend(loc="best")
    # Lq
    axis[0, 1].plot(x, Lq, linewidth=1.0, label=name_Lq)
    axis[0, 1].plot(x, Lq_e, linewidth=1.0, label=name_Lq_e)
    axis[0, 1].set_yscale('log')
    axis[0, 1].grid(linewidth = 0.5)
    axis[0, 1].legend(loc="best")
    # Ws
    axis[1, 0].plot(x, Ws, linewidth=1.0, label=name_Ws)
    axis[1, 0].plot(x, Ws_e, linewidth=1.0, label=name_Ws_e)
    axis[1, 0].set_yscale('log')
    axis[1, 0].grid(linewidth = 0.5)
    axis[1, 0].legend(loc="best")
    # Wq
    axis[1, 1].plot(x, Wq, linewidth=1.0, label=name_Wq)
    axis[1, 1].plot(x, Wq_e, linewidth=1.0, label=name_Wq_e)
    axis[1, 1].set_yscale('log')
    axis[1, 1].grid(linewidth = 0.5)
    axis[1, 1].legend(loc="best")
    plt.show()

def quardiPlotLin(
    x, 
    Ls, Ls_e,
    Lq, Lq_e,
    Ws, Ws_e,
    Wq, Wq_e,
    name_Ls, name_Ls_e,
    name_Lq, name_Lq_e,
    name_Ws, name_Ws_e,
    name_Wq, name_Wq_e):
    figure, axis = plt.subplots(2, 2, figsize=(8, 7))
    # Ls
    axis[0, 0].plot(x, Ls, linewidth=1.0, label=name_Ls)
    axis[0, 0].plot(x, Ls_e, linewidth=1.0, label=name_Ls_e)
    axis[0, 0].grid(linewidth = 0.5)
    axis[0, 0].legend(loc="best")
    # Lq
    axis[0, 1].plot(x, Lq, linewidth=1.0, label=name_Lq)
    axis[0, 1].plot(x, Lq_e, linewidth=1.0, label=name_Lq_e)
    axis[0, 1].grid(linewidth = 0.5)
    axis[0, 1].legend(loc="best")
    # Ws
    axis[1, 0].plot(x, Ws, linewidth=1.0, label=name_Ws)
    axis[1, 0].plot(x, Ws_e, linewidth=1.0, label=name_Ws_e)
    axis[1, 0].grid(linewidth = 0.5)
    axis[1, 0].legend(loc="best")
    # Wq
    axis[1, 1].plot(x, Wq, linewidth=1.0, label=name_Wq)
    axis[1, 1].plot(x, Wq_e, linewidth=1.0, label=name_Wq_e)
    axis[1, 1].grid(linewidth = 0.5)
    axis[1, 1].legend(loc="best")
    plt.show()

quardiPlotLog(
    n_Rho, 
    array_Plot_Ls, Ls_fnRho,
    array_Plot_Lq, Lq_fnRho, 
    array_Plot_Ws, Ws_fnRho, 
    array_Plot_Wq, Wq_fnRho, 
    "Ls", "Ls_e",
    "Lq", "Lq_e",
    "Ws", "Ws_e",
    "Wq", "Wq_e")

quardiPlotLin(
    n_Rho, 
    array_Plot_Ls, Ls_fnRho,
    array_Plot_Lq, Lq_fnRho, 
    array_Plot_Ws, Ws_fnRho, 
    array_Plot_Wq, Wq_fnRho, 
    "Ls", "Ls_e",
    "Lq", "Lq_e",
    "Ws", "Ws_e",
    "Wq", "Wq_e")'''