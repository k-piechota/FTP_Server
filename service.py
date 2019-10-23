import socket
import os
import sys

class Service():
	def __init__(self, client, addr):
		self.client = client
		self.addr = addr
		self.users =  self.load_users() 
		print('Thread for client:{} created.'.format(addr))
		self.login()
		self.run()
		
	def run(self):
		message = "What do you want to do? \n Type \"send\" to send file. Type \"get\" to download file."
		self.client.sendall(message.encode('utf-8'))
		data = self.client.recv(1024)
		data = data.decode('utf-8')
		data = data.strip()
		if data=="send":
			message = ""
			self.client.sendall(message.encode('utf-8'))
			self.download_file()
				
		elif data=="get":
			message = ""
			self.client.sendall(message.encode('utf-8'))
			self.send_file()
			
		elif data=="q":
			self.client.shutdown(socket.SHUT_RDWR)
			self.client.close()
			#thread.Thread_stop()
				
		else:
			message = "Unrecognized command"
			self.client.sendall(message.encode('utf-8'))
			
	def send_file(self):
		files = []
		files = os.listdir("server_files/")
		package = "Available files: "
		for x in files:
			package = package + x + " "
			
		package = package.encode('utf-8')	
		self.client.sendall(package)
		recv_data = self.client.recv(1024)
		file = recv_data.decode('utf-8').strip().split(",")
		file_location = "server_files/" + file[0]
		file_size = os.path.getsize(file_location)
		self.client.sendall("Exists,{}".format(file_size).encode('utf-8'))
		recv_data = self.client.recv(1024)
		with open(file_location, "rb") as file:
			self.client.sendfile(file)
		recv_data = self.client.recv(1024)
		print('Sent file {} to client {}'.format(file_location, self.addr))
		
		
	def download_file(self):
		recv_data = self.client.recv(1024)
		file_size = recv_data.decode('utf-8').strip().split(",")
		file_name = "file.txt"
		save_file = open("server_files\{}".format(file_name), "w+")
		amount_recieved_data = 0
		while amount_recieved_data < int(file_size[1]):
			recv_data = self.client.recv(1)
			amount_recieved_data += len(recv_data)
			save_file.write(recv_data.decode('utf-8'))
		save_file.close()
		print('Received file {} from client {}'.format(file_name, self.addr))

	
	
	def login(self):
		data = self.client.recv(1024)
		login_info = data.decode('utf-8').strip().split(",")
		print('{} - {}'.format(self.addr, login_info))
		user_info = login_info[0].split(":")
		pass_info = login_info[1].split(":")
		if user_info[1] in self.users:
				
				if (self.users[user_info[1]]==pass_info[1]) == True:
					message = "Authentication passed"
					self.client.sendall(message.encode('utf-8'))
				else:
					message = "Authentication failed. Disconnecting"
					self.client.sendall(message.encode('utf-8'))
					#self.client.shutdown(client.SHUT_RDWR)
					#self.client.close()
		else:
			message = "Authentication failed. Disconnecting"
			self.client.sendall(message.encode('utf-8'))
			sys.exit(1)
				
		
	def load_users(self):
		users = []
		with open("allowed_users.txt", "r") as user_file:
			users = user_file.readlines()
		users = [x.strip() for x in users]
		dict = {}
		for user in users:
			log = user.split(":")
			dict[log[0]] = log[1]
		return dict		