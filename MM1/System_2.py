'''
Working base eversion for demostration 

CONSIDERATIONS
The inter arrival time will never show up 0 becasue will show up the last IA and 
    if it show up something it means that a UT has pass thus the IA was not zero 

There is no need to cut the simulation both in the front or in the back because from the plot of pkgs in the system for ut
    is possible to see that if lambda < mu then there is no difference in any point of the graph 
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# variables generation and serving 
avg_poisson_gen = 5
avg_exp_serving = 4

# system variables 
print_dataframe = False
simulation_time = 1000

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
    
    def from_buffer_to_server(self, buffer):
        # FIFO buffer
        # get first pkg
        pkg = buffer.queue[0]
        # eliminate from queue
        buffer.queue.pop(0)
        # move into the server change server status
        self.status = 1
        self.pkg_serving = pkg

        # generate a serving time 
        self.serving_time = math.floor(np.random.exponential(avg_exp_serving))
        # initiate service progression 
        self.service_progression = 0
    
    def service(self, buffer, pkgs_served):
        # if status of the server is zero and a pkg in the buffer exits then move the pkg into the server
        if self.status == 0 and buffer.calculate_buffer_size() > 0:
            self.from_buffer_to_server(buffer)
        
        # if the serving time == 0 then after the from_buffer...() call the status will be 1 
        if self.status == 1:
            self.service_progression += 1
            if self.service_progression >= self.serving_time:
                # empty the server 
                self.status = 0
                self.serving_time = None
                self.service_progression = None

                # append in pkgs served
                pkgs_served.append(self.pkg_serving)
                # erase pkg given exited the server 
                self.pkg_serving = None

class System():
    def __init__(self, run_time):
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
        self.pkgs_for_unitTime = []

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
                # start inter arrival time 
                self.inter_arrival_time = np.random.poisson(avg_poisson_gen)
                # set generation progression to zero for initialize it 
                self.generation_progression = 0
            
            # increment only if self.inter_arrival_time != 0 because the pkg gen fn will be called again
            if self.inter_arrival_time != 0:
                self.generation_progression += 1
        else: 
            self.inter_arrival_time = None
            self.generation_progression = None
        
        return pkg 
        
    def simulation(self):
        df = pd.DataFrame(columns = [
            "unitTime", 
            "interTime", "genProc", "pkgIdGen", 
            "queue", "bufferDim",
            "serverStatus", "pkgIdServ", "servingTime", "serverProc",
            "nPkgsServed", "pkgsServed"])      

        # continue the process until all pks are served 
        while (
            (self.current_time < self.run_time) or 
            (self.buffer.calculate_buffer_size() > 0) or 
            (self.server.status != 0)
            ):

            # print system
            data_list = []
            data_list.append(self.current_time)
            data_list.append(self.inter_arrival_time)
            data_list.append(self.generation_progression)

            # --- --- --- start sys call --- --- --- 

            # if inter arrivale time == 0 then re generate a pkg be calling recursivly the function 
            while True:
                # menage generation 
                pkg = self.pkg_generation()
                # manage buffer 
                if pkg != None: self.buffer.queue.append(pkg)
                # contiue to append in the same UT until the gen time is 0
                if self.inter_arrival_time != 0:
                    break
            
            # manage server
            while True:
                self.server.service(self.buffer, self.pkgs_served)
                # cuntinue to serve while the service time is 0
                if self.server.serving_time != 0:
                    break

            # --- --- --- end sys call --- --- --- 

            # --- --- --- start print --- --- ---
            # print pkg
            if pkg == None: data_list.append(None)
            elif pkg != None: data_list.append(pkg.id_number)

            # print buffer
            queue_pkgs = []
            for i in range(len(self.buffer.queue)):
                queue_pkgs.append(self.buffer.queue[len(self.buffer.queue) - i - 1].id_number)
            data_list.append(queue_pkgs)
            data_list.append(self.buffer.calculate_buffer_size())

            # print server 
            printServerStatus = "-->" if self.server.status == 1 else "None"
            data_list.append(printServerStatus)

            # print pkg served 
            if self.server.pkg_serving == None: data_list.append(None)
            elif self.server.pkg_serving != None: data_list.append(self.server.pkg_serving.id_number)
            data_list.append(self.server.serving_time)
            data_list.append(self.server.service_progression)
            
            # print sys
            last_served_pkgs = []
            for i in range(len(self.pkgs_served)):
                if i >= 5: break
                last_served_pkgs.append(self.pkgs_served[len(self.pkgs_served) - i - 1].id_number)
            data_list.append(len(self.pkgs_served))
            data_list.append(last_served_pkgs)

            # append to the last index of df that is the len(df)
            df.loc[len(df)] = data_list

            # --- --- --- end print --- --- ---

            # --- --- --- start feedback --- --- ---

            self.pkgs_for_unitTime.append(self.n_pkgs - len(self.pkgs_served))

            # --- --- --- end feedback --- --- ---

            # increment simulation time 
            self.current_time += 1
        
        if print_dataframe == True:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.width', 300)  
            print(df)


pkgs_for_unitTime = System(simulation_time).pkgs_for_unitTime
Ls = round(np.mean(pkgs_for_unitTime), 2)

print("Ls: ", Ls)

ut = []
for i in range(len(pkgs_for_unitTime)):
    ut.append(i)

plt.plot(ut, pkgs_for_unitTime, color=(0, 0, 0), linewidth=1.0)
plt.grid(linewidth = 0.5)
plt.show()
