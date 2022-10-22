import random as rand
import pandas as pd

pkg_min_gen_time = 2
pkg_max_gen_time = 3
server_min_gen_time = 2
server_max_gen_time = 3

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
        self.server = Server()

        # start simulation
        self.simulation()

    def pkg_generation(self):
        global pkg_min_gen_time 
        global pkg_max_gen_time
        min_time = pkg_min_gen_time 
        max_time = pkg_max_gen_time
        # initialize pkg to none 
        pkg = None
        # generate pkg zero
        if self.current_time == 0:
            # what does it means to generate a pkg an object 
            pkg = Package()
            pkg.id_number = self.n_pkgs
            pkg.status = 0
            self.n_pkgs += 1

            self.inter_arrival_time = rand.randint(min_time, max_time)
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
                self.inter_arrival_time = rand.randint(min_time, max_time)

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
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 500)        

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
        
        print(df)


System(25)