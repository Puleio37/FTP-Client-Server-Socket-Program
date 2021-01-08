#Christian Puleio
#Sources
#- https://stackoverflow.com/questions/29058163/sending-files-between-client-server-through-tcp-socket-in-python
#- https://stackoverflow.com/questions/46790250/tcp-sockets-to-send-and-receive-files-using-python
#-https://stackoverflow.com/questions/13993514/sending-receiving-file-udp-in-python
import socket, sys, os

#these are the two command line input values
controlPort = int(sys.argv[1])
dataPort = int(sys.argv[2])

serverControl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creating socket for the control commands
serverControl.bind((socket.gethostname(), controlPort))#connects the command client socket and server socket  
serverControl.listen(1)#allows for one client to contact the server through the control socket 
print('Server control socket is listening...')#server is listening 

serverData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creating socket for the data
serverData.bind((socket.gethostname(), dataPort))#connects data the client socket and server socket  
serverData.listen(1)#allows for one client to contack the server through the data socket  
print('Server data socket is listening...')#server is listening 

while True:

	clientControl, controlAddress = serverControl.accept()
	print('[ACK] {0} conneted successful!'.format(controlAddress))	
	clientControl.send(bytes('[ACK] connected to server {0} {1} successful!').format(socket.gethostname(), controlPort))

	clientData, dataAddress = serverData.accept()
	print('[ACK] {0} conneted successful!'.format(dataAddress))
	clientData.send(bytes('[ACK] connected to server {0} {1} successful!').format(socket.gethostname(), dataPort))

	connection = True

	while connection:
		clientCommand = clientControl.recv(512)#recieving command from the client 
		clientCommand = clientCommand.decode('utf-8')#decoding it
		print('client sent: {}'.format(clientCommand))#shows what the client sent
		if(clientCommand == 'exit'):
			connection = False
			clientControl.send(bytes('[ACK] Closing connection... \n [CONNECTION TERMINATED]'))
			print('[ACK] {0} has been disconnected!'.format(controlAddress))

		elif(clientCommand[0:2] == 'cd'):#if its a cd command 
			command = clientCommand.split()#spits up the path and command 
			print('command[0]: {0} ; command[1]: {1}').format(command[0], command[1])
			path = command[1]#this is the path in a path variable
			os.chdir(path)#os libreary chdir to change the directory 
			clientControl.send(bytes('Now in {0}').format(os.getcwd()))#tells client what directory they are currently in 

		elif(clientCommand[0:2] == 'ls'):#if its a ls command
			command = clientCommand.split()#spits up the path and command 
			path = command[1]#this is the path in a path variable
			os.listdir(path)#os library listdir to show what is inside the directory
			clientControl.send(bytes('list of directories and files: {0}').format(os.listdir(path)))#tells client what in the directory 

		elif(clientCommand[0:3] == 'cwd'):
			print(os.getcwd())
			clientControl.send(bytes('current working directory: {0}').format(os.getcwd()))


		else:

			string = clientCommand.split(' ', 1)#spliting up the command and the path 

			if(string[0] == 'put'):
				dataPath = string[1]#making a variable of the path 
				dataPath = dataPath.split('/')#splitting up the path with a '/'
				dataFile = dataPath[-1]#gets the last file/directory of the path 

				with open(dataFile, 'wb') as file_to_write:#opens file and reads bytes as a file_to_send
					data = clientData.recv(1024)#waits for the data being sent from the client
					while True:
						file_to_write.write(data)#writes the data to the file 
						if len(data) < 1024: #it will break when data is less then 1024
							break
						else:
							data = clientData.recv(1024)#else keep recieving data 
				print 'Recieved Successfully'

			elif(string[0] == 'get'):
				dataPath = string[1]#making a variable of the path 
				dataPath = dataPath.split('/')#splitting up the path with a '/'
				dataFile = dataPath[-1]#gets the last file/directory of the path 

				with open(dataFile, 'rb') as file_to_send:#opens file and reads bytes as a file_to_send
					for	data in file_to_send:#for the data thats in each line 
						clientData.sendall(data)#send all of the data to client
				print 'Sent Successfully'




	
	



