import http.client, urllib
import datetime
import socket
import time
import threading 
import errno
import simplejson as json

HOST = "localhost"
PORT = 39998    
BUFFER_SIZE = 4096
ENCODING = "utf-8"
CONNECT_WAIT = 5
SOCKET_TIMEOUT = 5

class network_client_thread(threading.Thread):
    
	def __init__(self, callback, command_list):
		threading.Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(SOCKET_TIMEOUT)
		self.callback = callback
		self.command_list = command_list
		self.connected = False
		self.failed_to_connect = False

		
	def connect_to_server(self):
		while(self.connected is False):
			try:
				if(self.failed_to_connect is True):
					print("Reattempting connection..")
					self.sock.connect((HOST, PORT))
					self.connected = True
				else:
					print("Connecting to server..")
					self.sock.connect((HOST, PORT))
					self.connected = True
					
			except socket.error as socket_e:
				print(str(socket_e));
				if socket_e.errno == errno.ECONNREFUSED:
					print("Failed to connect to server..")
					print("Will try again every ", CONNECT_WAIT, " seconds.")
					self.failed_to_connect = True
					self.connected = False
					time.sleep(CONNECT_WAIT)
				if (socket_e.errno == errno.EISCONN):
					self.connected = True
					print("Ignoring open socket exception..")
			except Exception as exception:
				print (exception)
	
	def run(self):
		while(True):
			if(self.connected is False):
				self.connect_to_server()
		
			try:
				data = self.sock.recv(BUFFER_SIZE)
				while len(data):
					print("cback")
					self.callback(self, data.decode(ENCODING))
					print("1")
					data = self.sock.recv(BUFFER_SIZE)
					print("2")
					data = self.sock.recv(BUFFER_SIZE)
					print("3")
			except socket.error as socket_e:
				if(socket_e.errno == None):
					print(socket_e)
					self.send_message("check", "")
				else:
					self.connected = False
					print(socket_e, socket_e.errno)				
	def send_message(self,command, data):
		message = command + "|" + data
		self.sock.sendall(message.encode())

def command_handler(self, raw_command):

#       if(len(raw_command) > 50):
#               response = "[+] Command to long..\n"
#               self.socket.send(response.encode())
		print(raw_command)
		processed_command = parse_raw_command(raw_command)
		print(processed_command)
		processed_data = parse_raw_command_data(raw_command)
		print(processed_data)

		if(processed_command in self.command_list):
			self.command_list[processed_command](self, json.loads(processed_data))

def parse_raw_command(raw_command):
        processed_command = ""

        if('\n' in raw_command):
                pipe_index = raw_command.find('|')
                processed_command = raw_command[:pipe_index]
        return processed_command

def parse_raw_command_data(raw_command):
        processed_data = ""

        if('\n' in raw_command and '|' in raw_command):
                pipe_index = raw_command.find('|')
                newline_index = raw_command.find('\n')
                processed_data = raw_command[pipe_index + 1:newline_index - 1]
        return processed_data


def test_function(data):
	print(data)
	print("yo yo yo yo")

clist = {"test" : test_function}
client_thrd = network_client_thread(command_handler, clist)
client_thrd.start()
	
