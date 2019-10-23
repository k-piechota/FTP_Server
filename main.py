
from client import Client
from server import Server

def main():
	val = input('Type: S to launch server else will launch client: ')
	if val == "s":
		serv = Server()
	else:
		clien = Client()
if __name__ == '__main__':
    main()
