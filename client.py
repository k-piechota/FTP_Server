import socket
import os
import sys
class Client():
	def __init__(self):
		self.PORT = 21
		self.connect()
		self.login()
		self.run()
		
	def connect(self):
		print('You must log in. \nIP:')
		HOST = input()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST, self.PORT))
		
		
	def login(self):
		print('Login:')
		login = input()
		print('Password:')
		passwd =  input()
		packet = "user:{},passwd:{}".format(login, passwd)
		self.s.sendall(packet.encode('utf-8'))
		data = self.s.recv(1024)
		print(data)
		
		
		
	def run(self):
		
		data = self.s.recv(1024)
		print(data)
		decision = input()
		self.s.sendall(decision.encode('utf-8'))
		if(decision == 'get'):
			self.download_file()
		if(decision == 'send'):
			self.send_file()
						
		
	def download_file(self):
		recv_data = self.s.recv(1024)
		files = recv_data.decode('utf-8').strip().split(",")
		print(files)
		file_name = self.file
		self.s.sendall(file_name.encode('utf-8'))

		recv_data = self.s.recv(1024)
		file_size = recv_data.decode('utf-8').strip().split(",")
		save_file = open("client_files\\{}.txt".format(self.id), "w+")
		amount_recieved_data = 0
		self.s.sendall(("Confirmed").encode('utf-8'))
		while amount_recieved_data < float(file_size[1]):
			recv_data = self.s.recv(1)
			amount_recieved_data += len(recv_data)
			save_file.write(recv_data.decode('utf-8'))
		message = 'Downloaded succesfully'
		print(message)
		self.s.sendall(message.encode('utf-8'))
		save_file.close()
		

		
		
	def send_file(self):
		files = []
		files = os.listdir("client_files")
		print(files)
		
		file_location = "file1.txt"
		file_size = os.path.getsize(file_location)
		self.s.sendall("Sending,{}".format(file_size).encode('utf-8'))
		with open(file_location, "rb") as file:
			self.s.sendfile(file)
		#self.s.close()
		