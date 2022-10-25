import random as rand
import pandas as pd
import numpy as np


avg_poisson_gen = 5
avg_exp_serveing = 4

print_dataframe = True
simulation_time = 250
n_experiments = 10

save_after_simulation = False

class Package:
    def __init__(self):
        self.id_number = None
        self.status = None

class Buffer:
    def __init__(self):
        self.queue = []
    
    def calculate_buffer_size(self):
        return len(self.queue)

class Server:
    def __init__(self, run_time, current_time):
        self.run_time = run_time
        self.current_time = current_time

        self.pkg_serving = None
        self.status = 0
        self.time_to_service = None
        self.service_progression = None

        # parameters
        self.array_serving_times = []
    
    def buffer_to_server(self, buffer):
        # FIFO buffer
        # get first pkg
        pkg = buffer.queue[0]
        # eliminate from queue
        buffer.queue.pop(0)
        # move into the server change pkg and server status
        self.status = 1
        self.pkg_serving = pkg
        pkg.status = 2

        self.time_to_service = np.random.exponential(avg_exp_serveing) + 1
        # save time 
        if save_after_simulation == True:
            self.array_serving_times.append(self.time_to_service)
        elif save_after_simulation == False:
            if self.current_time <= self.run_time:
                self.array_serving_times.append(self.time_to_service)

    def service(self, buffer, pkgs_served):
        # if the pkg exits in the buffer 
        if self.status == 0 and buffer.calculate_buffer_size() > 0:
            self.buffer_to_server(buffer)

        if self.status == 1:
            if self.service_progression == None:
                self.service_progression = 0
            if self.service_progression < self.time_to_service:
                self.service_progression += 1
            if self.service_progression >= self.time_to_service:
                # status of server 
                self.status = 0
                self.time_to_service = None
                self.service_progression = None
                # change status of pkg and add to the list of pkg served 
                self.pkg_serving.status = 3
                pkgs_served.append(self.pkg_serving)
                # erase pkg given exited the server 
                self.pkg_serving = None

                # add the one next in the buffer 
                if buffer.calculate_buffer_size() > 0:
                    self.buffer_to_server(buffer)

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
        self.server = Server(self.run_time, self.current_time)

        # parameters
        self.array_interArrival_times = []
        self.array_pkgsUt_queue = []
        self.array_pkgsUt_system = []
        self.dict_pkgsTime_queue = {}
        self.dict_pkgsTime_system = {}

        # start simulation
        self.simulation()

    def pkg_generation(self):
        # initialize pkg to none 
        pkg = None
        # generate pkg zero
        if self.current_time == 0:
            # what does it means to generate a pkg an object 
            pkg = Package()
            pkg.id_number = self.n_pkgs
            pkg.status = 0
            self.n_pkgs += 1

            self.inter_arrival_time = np.random.poisson(avg_poisson_gen) + 1
            # save time and decide to save all or only simulation generation time 
            if save_after_simulation == True:
                self.array_interArrival_times.append(self.inter_arrival_time)
            elif save_after_simulation == False:
                if self.current_time <= self.run_time:
                    self.array_interArrival_times.append(self.inter_arrival_time)

            self.generation_progression = 0
            self.generation_progression += 1
        elif self.current_time < self.run_time:
            if self.generation_progression >= self.inter_arrival_time:
                # then anohter pkg is created 
                pkg = Package()
                pkg.id_number = self.n_pkgs
                pkg.status = 0
                self.n_pkgs += 1

                self.generation_progression = 0
                self.inter_arrival_time = np.random.poisson(avg_poisson_gen) + 1
                # save time
                if save_after_simulation == True:
                    self.array_interArrival_times.append(self.inter_arrival_time)
                elif save_after_simulation == False:
                    if self.current_time <= self.run_time:
                        self.array_interArrival_times.append(self.inter_arrival_time)

            self.generation_progression += 1
        elif self.current_time >= self.run_time:
            self.inter_arrival_time = None
            self.generation_progression = None

        return pkg 
    
    def simulation(self):
        df = pd.DataFrame(columns = [
            "unitTime", 
            "interTime", "genProc", "pkgIdGen", 
            "bufferDim", "queue",
            "serverStatus", "pkgIdServ", "servingTime", "serverProc",
            "nPkgsServed", "pkgsServed"])      

        # continue the process until all pks are served 
        while (
            (self.current_time < self.run_time) or 
            (self.buffer.calculate_buffer_size() > 0) or 
            (self.server.status != 0)):

            # print system
            data_list = []
            data_list.append(self.current_time)
            data_list.append(self.inter_arrival_time)
            data_list.append(self.generation_progression)

            # --- --- --- start sys call --- --- --- 
            # menage generation 
            pkg = self.pkg_generation()

            # manage buffer 
            if pkg != None:
                pkg.status = 1
                self.buffer.queue.append(pkg)
            

            
            # server call

            self.server.service(self.buffer, self.pkgs_served)


            # --- --- --- end sys call --- --- --- 
            
            '''
            # --- --- --- start sys call --- --- --- 
            while True:
                # menage generation 
                pkg = self.pkg_generation()

                # manage buffer 
                if pkg != None:
                    pkg.status = 1
                    self.buffer.queue.append(pkg)
                
                if self.inter_arrival_time != 0:
                    break
            
            # server call
            while True:
                self.server.service(self.buffer, self.pkgs_served)
                if self.server.time_to_service != 0:
                    break

            # --- --- --- end sys call --- --- --- 
            '''
            def sys_info():
                # calculate how many pks in the system 
                n_pkgsUt_queue = len(self.buffer.queue)
                n_pkgsUt_system = self.server.status + n_pkgsUt_queue
                self.array_pkgsUt_queue.append(n_pkgsUt_queue)
                self.array_pkgsUt_system.append(n_pkgsUt_system)
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
            
            if save_after_simulation == True:
                sys_info()
            elif save_after_simulation == False:
                if self.current_time <= self.run_time:
                    sys_info()
                    
            # --- --- --- print end of unit time --- --- ---
            # print pkg
            if pkg == None: data_list.append(None)
            elif pkg != None: data_list.append(pkg.id_number)

            # print buffer
            data_list.append(self.buffer.calculate_buffer_size())
            queue_info = []
            for i in range(len(self.buffer.queue)):
                queue_info.append(self.buffer.queue[len(self.buffer.queue) - i - 1].id_number)
            data_list.append(queue_info)

            # print server 
            printServerStatus = "work" if self.server.status == 1 else 0
            data_list.append(printServerStatus)
            # print pkg
            if self.server.pkg_serving == None: data_list.append(None)
            elif self.server.pkg_serving != None: data_list.append(self.server.pkg_serving.id_number)
            data_list.append(self.server.time_to_service)
            data_list.append(self.server.service_progression)
            
            # print sys
            pkgs_info = []
            for i in range(len(self.pkgs_served)):
                if i >= 5: break
                pkgs_info.append(self.pkgs_served[len(self.pkgs_served)-i-1].id_number)
            data_list.append(len(self.pkgs_served))
            data_list.append(pkgs_info)

            # append to the last index of df that is the len(df)
            df.loc[len(df)] = data_list

            self.current_time += 1
        
        if print_dataframe == True:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.width', 300)  
            print(df)
    
    def calculate_parameters(self):
        # eliminate last element from array interArrival because the 
        #   in any case the simulation stopped and the last has not generate a pkg 
        mean_interArrival_time = round(np.mean(self.array_interArrival_times[:-1]), 2)
        mean_serving_time = round(np.mean(self.server.array_serving_times[:-1]), 2)
        sysLambda = round(1 / mean_interArrival_time, 2)
        sysMu = round(1 / mean_serving_time, 2)
        sysRho = round(sysLambda / sysMu, 2)
        Ls = round(np.mean(self.array_pkgsUt_system), 2)
        Lq = round(np.mean(self.array_pkgsUt_queue), 2)
        # for calculate time of pkg in the system have a dictionary 
        #   with every pkg generated and a loop that increase its time until served 
        # take all values of the dics and make an average 
        array_waitingTime_queue = []
        array_waitingTime_server = []
        for values in self.dict_pkgsTime_queue.values():
            array_waitingTime_queue.append(values)
        for values in self.dict_pkgsTime_system.values():
            array_waitingTime_server.append(values)
        Wq = round(np.mean(array_waitingTime_queue))
        Ws = Wq + round(np.mean(array_waitingTime_server))
        
        print("Inter Arrival Time: {}, Lambda: {}".format(mean_interArrival_time, sysLambda))
        print("Serving Time: {}, Mu: {}".format(mean_serving_time, sysMu))
        print("Rho: ", sysRho)
        print("Lq: ", Lq)
        print("Ls: ", Ls)
        print("Wq: ", Wq)
        print("Ws: ", Ws)
        return sysLambda, sysMu, Lq, Ls, Wq, Ws


sysLambda = []
sysMu = []
Lq = []
Ls = []
Wq = []
Ws = []

for i in range(n_experiments):
    sysLambdaVal, sysMuVal, LqVal, LsVal, WqVal, WsVal = System(simulation_time).calculate_parameters()

    sysLambda.append(sysLambdaVal)
    sysMu.append(sysMuVal)
    Lq.append(LqVal)
    Ls.append(LsVal)
    Wq.append(WqVal)
    Ws.append(WsVal)

sysLambdaVal = np.mean(sysLambda)
sysMyVal = np.mean(sysMu)
LqVal = np.mean(Lq)
LsVal = np.mean(Ls)
WqVal = np.mean(Wq)
WsVal = np.mean(Ws)
print(sysLambdaVal)
print(sysMuVal)
print(LqVal)
print(LsVal)
print(WqVal)
print(WsVal)

    
