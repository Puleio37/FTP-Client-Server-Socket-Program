#Christian Puleio
#Sources
#- https://stackoverflow.com/questions/29058163/sending-files-between-client-server-through-tcp-socket-in-python
#- https://stackoverflow.com/questions/46790250/tcp-sockets-to-send-and-receive-files-using-python
#-https://stackoverflow.com/questions/13993514/sending-receiving-file-udp-in-python
import socket, sys, os

#these are the three command line input values
localhost = sys.argv[1]
controlPort = int(sys.argv[2])
dataPort = int(sys.argv[3])

clientControl = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creating socket for the control commands
clientControl.connect((socket.gethostname(), controlPort))#creating a connection to the server with the contol socket 
print('[CONTROL PORT CONNECTED] Connected to {0} {1}'.format(localhost, controlPort))#Acknowledegment that it connected to localhost

clientData = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creating socket for the Data
clientData.connect((socket.gethostname(), dataPort))#creating a connection to the server with the Data socket
print('[DATA PORT CONNECTED] Connected to {0} {1}'.format(localhost, dataPort))#Acknowledegment that it connected to localhost

clientControlACK = clientControl.recv(512)#Ackknowledgement from server for control socket connection
clientControlACK = clientControlACK.decode('utf-8')#decode of acknowledgement
print(clientControlACK)
	
clientDataACK = clientData.recv(512)#Ackknowledgement from server for data socket connection
clientDataACK = clientDataACK.decode('utf-8')#decode of acknowledgement
print(clientDataACK)

while True: 

	command = str(raw_input('Enter a command: ' ))#command input

	string = command.split(' ', 1)#spliting up the command and the path 

	if(string[0] == 'put'):#if its a put command
		clientControl.send(bytes(command.encode('utf-8')))#sends over full command
		inputPath = string[1]#making a variable of the path 
		inputPath = inputPath.split('/')#splitting up the path with a '/'
		inputFile = inputPath[-1]#gets the last file/directory of the path 

		with open(inputFile, 'rb') as file_to_send:#opens file and reads bytes as a file_to_send
			for data in file_to_send:#for the data thats in each line 
				clientData.sendall(data)#send all of the data to server
		print('put successful')#success acknowledgement 
	
	elif(string[0] == 'get'):#if its a get command
		clientControl.send(bytes(command.encode('utf-8')))#sends over full command
		inputPath = string[1]#making a variable of the path 
		inputPath = inputPath.split('/')#splitting up the path with a '/'
		inputFile = inputPath[-1]#gets the last file/directory of the path 

		with open(inputFile, 'wb') as file_to_write:#opens file and writes bytes as a file_to_write
			data = clientData.recv(1024)#waits for the data being sent from the server 
			while True: 
				file_to_write.write(data)#writes the data to the file 
				if len(data) < 1024: #it will break when there is no data
					break
				else:
					data = clientData.recv(1024)#else the client will continue to accept data 
		print('get successful')#success acknowledgement  
	else:

		#for ls and cd
		clientControl.send(bytes(command.encode('utf-8')))#sends commands
		messageControl = clientControl.recv(512)#gets information back from server
		messageControl = messageControl.decode('utf-8')#decodes it
		print(messageControl)#shows it







