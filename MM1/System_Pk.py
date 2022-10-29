
'''
No zero 
Loop experiments
No runtime 
Better calculation W
'''

import matplotlib.pyplot as plt
import numpy as np
import math

# costant serving variable
IA = 12
S = 6

# system variables 
print_dataframe = False
print_graphs = False
simulation_time = 4000
n_experiments = 1

np.random.seed(4269)

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
            self.serving_time =  math.floor(np.random.exponential(S))
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
            if self.service_progression >= self.serving_time:
                # append in pkgs served
                pkgs_served.append(self.pkg_serving)

                self.status = 0

class System():
    def __init__(self, run_time, avg_exp_generation):
        self.avg_exp_generation = avg_exp_generation
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

        # start simulation
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
                    self.inter_arrival_time = math.floor(np.random.exponential(IA)) 
                    if  self.inter_arrival_time > 0:
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

            # print system
            data_list = []
            data_list.append(self.current_time)
            data_list.append(self.inter_arrival_time)
            data_list.append(self.generation_progression)

            # --- --- --- start sys call --- --- --- 
            # generation call
            pkg = self.pkg_generation()
            # buffer call
            if pkg != None: self.buffer.queue.append(pkg)
            # server call
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

        

        '''print(array_waitingTime_queue)
        print(len(array_waitingTime_queue))
        print(np.mean(array_waitingTime_queue))'''
        '''print()
        print(array_waitingTime_queue)
        print(len(array_waitingTime_queue))
        print(np.mean(array_waitingTime_queue))
        print(self.dict_pkgsTime_queue)
        print(self.n_pkgs)
        new_array = array_waitingTime_queue
        for n in range(self.n_pkgs - len(array_waitingTime_queue)):
            print("yesdkjlf")
            new_array.append(0.3)
        print(new_array)
        print(len(new_array))
        print(np.mean(new_array))
        print()'''

        return (
            self.array_inter_arrival_time,
            self.server.array_serving_time,
            self.pkgs_sys_for_unitTime,  
            self.pkgs_queue_for_unitTime,
            array_waitingTime_server,
            array_waitingTime_queue,
            self.array_P01
            )


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
    Ls = np.mean(pkgs_sys_for_unitTime)
    Lq = np.mean(pkgs_queue_for_unitTime)
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

    print("--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---", i)
    print("*** *** Theo Values *** ***")
    print("avg InterArrival theo: ", IA)
    print("avg Serving theo: ", S)
    print("Lambda theo: ", round(Lambda_theo, 2))
    print("Mu theo: ", round(Mu_theo, 2))
    print("Rho theo: ", round(Rho_theo, 2))
    print("Ls theo: ", round(Ls_theo, 2))
    print("Lq theo: ", round(Lq_theo, 2))
    print("Ws theo: ", round(Ws_theo, 2))
    print("Wq theo: ", round(Wq_theo, 2))
    print("P0 theo: ", round(P0_theo, 2))
    print("*** *** Experimental Values *** ***")
    print("avg InterArrival: ", round(avg_interArrival, 2))
    print("avg serving: ", round(avg_serving, 2))
    print("Lambda: ", round(Lambda, 2))
    print("Mu: ", round(Mu, 2))
    print("Rho: ", round(Rho, 2))
    print("Ls: ", round(Ls, 2))
    print("Lq: ", round(Lq, 2))
    print("Ws: ", round(Ws, 2))
    print("Wq: ", round(Wq, 2))
    print("P0: ", round(P0, 2))

    # prints of hist and Ls of 1 experiment
    if print_graphs == True:
        plt.hist(array_serving_time, bins=30) 
        plt.hist(array_inter_arrival_time, bins=30) 
        plt.show() 

        ut = []
        for i in range(len(pkgs_sys_for_unitTime)):
            ut.append(i)

        plt.plot(ut, pkgs_sys_for_unitTime, color=(0, 0, 0), linewidth=1.0)
        plt.title("Pkgs for Unit Time")
        plt.ylabel("Pkgs")
        plt.xlabel("UT")
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

# mantenendo un Rho costante e cambiando k 
Pk_theo = []
Pk = []
k = []
for i in range(15):
    k.append(i)
    Pk_theo.append(P0_theo * (Rho_theo ** i))
    Pk.append(out_P0 * (out_Rho ** i))
print(k)
print(Pk_theo)
print(Pk)

plt.plot(k, Pk_theo, linewidth=1.0, color=(0, 0, 0), label="Pk")
plt.plot(k, Pk, linewidth=1.0, color=(0, 0, 0), linestyle = 'dashed', label="Pk exp")
plt.ylabel("Pk")
plt.xlabel("k")
plt.grid(linewidth = 0.5)
plt.legend(loc="best")
plt.show()







