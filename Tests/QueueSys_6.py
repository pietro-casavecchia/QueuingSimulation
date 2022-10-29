import random as rand
import pandas as pd
import numpy as np
import math

labda = 0.5


server_min_gen_time = 10
server_max_gen_time = 10

print_dataframe = True
simulation_time = 30

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
    def __init__(self):
        global server_min_gen_time 
        global server_max_gen_time
        self.min_time = server_min_gen_time 
        self.max_time = server_max_gen_time 

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

        self.time_to_service = rand.randint(self.min_time, self.max_time)
        # save time 
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
        self.interArrival_time = None

        # generate a buffer and server
        self.buffer = Buffer()
        self.server = Server()

        # parameters
        self.array_interArrival_times = []
        self.array_pkgsUt_queue = []
        self.array_pkgsUt_system = []
        self.dict_pkgsTime_queue = {}
        self.dict_pkgsTime_system = {}

        # start simulation
        self.simulation()
        # statistics
        self.calculate_parameters()
    
    def poisson_arrival(self, labda, interArrival_time):
        # PDF of tau equal to time 
        PDF = round(labda * math.pow(math.e, -(labda * interArrival_time)), 2)
        # simulate probabiliy 
        throw = rand.randint(0, 100) / 100
        # test if throw <= then PDF then pkg is generated 
        if throw <= PDF:
            print(throw, PDF)
            return True
    
    def generate(self):
        pkg = Package()
        pkg.id_number = self.n_pkgs
        pkg.status = 0
        self.n_pkgs += 1
        self.interArrival_time = 0
        return pkg

    def pkg_generation(self):
        global labda
        labda = labda
        # initialize pkg to none 
        pkg = None
        # generate pkg zero
        if self.current_time == 0:
            pkg = self.generate()
            # save time
            self.array_interArrival_times.append(self.interArrival_time)
        elif self.current_time < self.run_time:
            self.interArrival_time += 1
            pkg_generated = self.poisson_arrival(labda, self.interArrival_time)
            print(self.interArrival_time, pkg_generated)
            if pkg_generated == True:
                # save time
                self.array_interArrival_times.append(self.interArrival_time)
                # then anohter pkg is created and inter time is set to zero 
                pkg = self.generate()
        elif self.current_time >= self.run_time:
            self.interArrival_time = None

        return pkg 
    
    def simulation(self):
        df = pd.DataFrame(columns = [
            "unitTime", 
            "interTime", "pkgIdGen", 
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
            data_list.append(self.interArrival_time)
            
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
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 500)  
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

        


System(simulation_time)