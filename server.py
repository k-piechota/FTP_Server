import socket
import csv
import os
import threading
from multiprocessing import Process
from service import Service

class Server():
	def __init__(self):
		HOST = socket.gethostname()
		PORT = 21
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (HOST, PORT)
		s.bind(('', PORT))
		s.listen()
		ip, portt = s.getsockname()
		print("Server has started listening... ip: {}, port: {}".format(ip, portt))
		while True:
				client, addr = s.accept()	
				print('Connected by', addr)
				x= Process(target=Service, args=(client,addr))
				x.start()

			
		
		
	