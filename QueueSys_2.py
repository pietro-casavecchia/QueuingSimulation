import random as rand
import pandas as pd

pkg_min_gen_time = 1
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

    def service(self, buffer, pkgs_served):
        # if the pkg exits in the buffer 
        if self.status == 0 and buffer.calculate_buffer_size() > 0:
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
            "interTime", "genProcess", "pkgId", "pkgStatus",
            "bufferDim", "queue", 
            "serverStatus", "servingTime", "serverProcess", 
            "nPkgsServed", "pkgsServed"])
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 500)        

        # continue the process until all pks are served 
        while (
            (self.current_time < self.run_time) or 
            (self.buffer.calculate_buffer_size() > 0) or 
            (self.server.status != 0)):

            # print 
            data_list = []
            data_list.append(self.current_time)
            data_list.append(self.inter_arrival_time)
            data_list.append(self.generation_progression)

            # finish generation after run time 
            pkg = self.pkg_generation()

            # manage buffer 
            if pkg == None: data_list.extend([None, None])
            if pkg != None:
                pkg.status = 1
                self.buffer.queue.append(pkg)
                data_list.extend([pkg.id_number, pkg.status])

            # server call
            self.server.service(self.buffer, self.pkgs_served)
            
            # *** *** *** print 
            data_list.append(self.buffer.calculate_buffer_size())
            queue_info = []
            for i in range(len(self.buffer.queue)):
                queue_info.append(self.buffer.queue[i].id_number)
            data_list.append(queue_info)

            data_list.append(self.server.status)
            data_list.append(self.server.time_to_service)
            data_list.append(self.server.service_progression)

            pkgs_info = []
            n_pkgs_served = 0
            for i in range(len(self.pkgs_served)):
                if i >= 5: break
                pkgs_info.append(self.pkgs_served[len(self.pkgs_served)-i-1].id_number)
                n_pkgs_served += 1
            data_list.append(n_pkgs_served)
            data_list.append(pkgs_info)

            # append to the last index of df that is the len(df)
            df.loc[len(df)] = data_list

            self.current_time += 1
        
        print(df)


System(25)