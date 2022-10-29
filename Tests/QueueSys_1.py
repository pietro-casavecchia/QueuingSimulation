import random as rand

from matplotlib.widgets import Button

class Buffer:
    def __init__(self):
        self.n_pkg = 0

class Package:
    def __init__(self):
        self.min_time = 1
        self.max_time = 3
        self.id_number = None
        self.status = None
        self.arrival_time = None
        self.service_time = None
        self.departed_time = None
    
    def generate_pkg(self):

        

class Server: 
    def __init__(self):
        self.min_time = 1
        self.max_time = 3
        self.status = 0
        self.time_to_service = None
        self.service_progression = None

    def service(self, pkg):
        print("status: {}, time to service: {}, service progress: {}".format(
                self.status, self.time_to_service, self.service_progression))
        if self.status == 0 and pkg == True:
            # the server is empty
            # a pkg is ready to be process
            self.status = 1
            # generate time to service for this pkg
            self.time_to_service = rand.randint(self.min_time, self.max_time)
        # from 0 -> 1 without waiting for another unit of time
        if self.status == 1:
            if self.service_progression == None:
                self.service_progression = 1
            elif self.service_progression < self.time_to_service:
                self.service_progression += 1
            else:
                # reset variabiles
                self.status = 0
                self.time_to_service = None
                self.service_progression = None

class System:
    def __init__(self, simulation_life, n_servers):
        self.simulation_life = simulation_life
        self.n_servers = n_servers
        self.current_time = 0
        self.pkg = Package()
        self.buffer = Buffer()
        self.servers = []
        self.create_servers() 
        self.run_time()
    
    def create_servers(self):
        for i in range(self.n_servers):
            self.servers.append(Server())

    def manage_buffer(self):
        pass
    
    def run_time(self):
        while self.current_time < self.simulation_life: 
            # generate pkg
            
            # call the server class
            self.servers[0].service(True)
            # increment time 
            self.current_time += 1
            print("*** {} of {} ***".format(self.simulation_life, self.current_time))


mainSystem = System(10, 1)



