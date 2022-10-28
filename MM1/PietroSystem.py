import math
import random

import numpy as np

DEBUG = True
VERBOSE = True
clock = 0
avg_gen_time = 5
avg_ser_time = 3


class Stats:
	def _init_(self):
		self.num_pkt_queue = 0
		self.num_pkt_server = 0

	def get_avg_pkt_system(self):
		return (self.num_pkt_queue + self.num_pkt_server) / clock

	def get_avg_pkt_queue(self):
		return self.num_pkt_queue / clock

	def _str_(self):
		return "Stats [Ls={}, Lq={}, Ws={}, Wq={}]".format(self.get_avg_pkt_system(), self.get_avg_pkt_queue(), 0, 0)


def gen_function(x):
	y = 0
	while y < 1: y = np.random.exponential(x)
	return math.floor(y)


class Packet:
	def _init_(self, uid: int):
		self.uid = uid  # Packet number


class Queue:
	def _init_(self):
		self.queue = []

	def size(self):
		return len(self.queue)

	def empty(self):
		return self.size() < 1

	def extract(self):
		if not self.empty():
			return self.queue.pop(0)
		else: return None  # The queue is empty

	def enqueue(self, pkt: Packet):
		if pkt is not None:
			self.queue.append(pkt)
		else:
			print("[E] Queue: received a null packet")

	def _str_(self):
		if self.empty(): return "Queue []"
		inverted = self.queue.copy()
		inverted.reverse()
		s = "Queue ["
		first = True
		for pkt in inverted:
			if first:
				s += str(pkt.uid)
				first = False
			else:
				s += ", " + str(pkt.uid)
		s += "]"
		return s


class Server:
	def _init_(self, avg_time):
		self.time_left = None
		self.avg_time = avg_time
		self.pkt = None

	def tick(self):
		if self.working():
			if self.time_left == 0:  # Packet ready to be served
				self.serve()
			else:
				self.time_left -= 1  # Packet needs to be worked

	def serve(self):
		if DEBUG: print("[I] Server: finished pkt_id={}".format(self.pkt.uid))
		self.pkt = None
		self.time_left = None

	def working(self):
		return self.pkt is not None

	def idle(self):
		return self.pkt is None

	def send(self, pkt):
		if self.idle():
			if pkt is not None:
				self.pkt = pkt
				self.time_left = gen_function(self.avg_time)
				if DEBUG: print("[I] Server: received pkt_id={}, t_left={}".format(self.pkt.uid, self.time_left))
			else:
				print("[E] Server: packet is null")
		else:
			print("[E] Server: packet sent but server is busy")

	def _str_(self):
		if self.working():
			return "Server [state=WORKING, pkt_id={}, t_left={}]".format(self.pkt.uid, self.time_left)
		else:
			return "Server [state=IDLE]"


class System:
	def _init_(self, queue: Queue, server: Server, stats: Stats):
		self.queue = queue
		self.server = server
		self.stats = stats

	def tick(self):
		if not self.queue.empty():
			if self.server.idle():
				new_pkt = self.queue.extract()
				self.server.send(new_pkt)

		self.server.tick()

		self.stats.num_pkt_queue += self.queue.size()
		self.stats.num_pkt_server += int(self.server.working())

	def send(self, pkt: Packet):
		if pkt is not None:
			self.queue.enqueue(pkt)
			if DEBUG: print("[I] System: queue received pkt_id={}".format(pkt.uid))
		else:
			print("[E] System: queue received a null packet")


def main():
	global clock
	seed = random.randint(1, 1000)
	np.random.seed(seed)
	print("[I] Seed set to", seed)

	# Create all the system objects
	stats = Stats()
	q = Queue()
	s = Server(avg_ser_time)
	sys = System(q, s, stats)

	time_left = gen_function(avg_gen_time)  # Generate the time for generating the first packet
	pkt_num = 0
	if DEBUG: print("[I] Main: generating first pkt_id={} t_left={}".format(pkt_num, time_left))

	clock = 0
	clock_max = 10000
	while clock < clock_max:
		if time_left == 0:  # If the packet is ready to be sent
			pkt = Packet(pkt_num)                       # Generate
			sys.send(pkt)                               # Send to the queue
			pkt_num += 1                                # Increase paket count for IDs
			time_left = gen_function(avg_gen_time)      # Get the time needed for the next generation
			if DEBUG: print("[I] Main: generating pkt_id={} t_left={}".format(pkt_num, time_left))

		# Make the system go forward
		sys.tick()

		# Print useful data
		if VERBOSE: print("\n>>>", clock)
		if VERBOSE: print(q)
		if VERBOSE: print(s)

		# Increase/decrease counters
		time_left -= 1
		clock += 1

	lambda_th = 1 / avg_gen_time
	mu_th = 1 / avg_ser_time
	rho_th = lambda_th / mu_th
	ls_th = rho_th / (1 - rho_th)
	lq_th = (lambda_th * lambda_th) / (mu_th * (mu_th - lambda_th))
	ws_th = 1 / (mu_th - lambda_th)
	wq_th = lambda_th / (mu_th * (mu_th - lambda_th))
	print()
	print(stats)
	print("Ideal [Ls={}, Lq={}, Ws={}, Wq={}]".format(
		round(ls_th, 2),
		round(lq_th, 2),
		round(ws_th, 2),
		round(wq_th), 2)
	)

	ls_err = (ls_th - stats.get_avg_pkt_system()) / ls_th
	lq_err = (lq_th - stats.get_avg_pkt_queue()) / lq_th
	print("Errore Ls: {}%".format(round(ls_err*100)))
	print("Errore Lq: {}%".format(round(lq_err*100)))


if __name__ == '__main__':
	main()