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

buf = 1024
server_address = ('localhost', dataPort)

clientControl = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creating socket for the control commands
clientControl.connect((socket.gethostname(), controlPort))#creating a connection to the server with the contol socket 
print('[CONTROL PORT CONNECTED] Connected to {0} {1}'.format(localhost, controlPort))#Acknowledegment that it connected to localhost

clientData = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#creating socket for the Data

clientControlACK = clientControl.recv(512)#Acknowledgement from server for control socket connection
clientControlACK = clientControlACK.decode('utf-8')	#decode of acknowledgement
print(clientControlACK)
	
while True: 

	command = str(raw_input('Enter a command: ' ))#command input

	string = command.split(' ', 1)#spliting up the command and the path 

	if(string[0] == 'put'):#if its a put command
		clientControl.send(bytes(command.encode('utf-8')))#sends over full command
		inputPath = string[1]#making a variable of the path 
		inputPath = inputPath.split('/')#splitting up the path with a '/'
		inputFile = inputPath[-1]#gets the last file/directory of the path 
		clientData.sendto(inputFile, server_address)

		with open(inputFile, 'rb') as file_to_send:#opens file and reads bytes as a file_to_send
			data = file_to_send.read(buf)#reading the file 
			while(data):#while data 
				if(clientData.sendto(data, server_address)):#will keep sending data 
					print 'sending...'
					data = file_to_send.read(buf)#keep reading the file
			
				print('put successful')
	
	elif(string[0] == 'get'):#if its a get command
		clientControl.send(bytes(command.encode('utf-8')))#sends over full command
		inputPath = string[1]#making a variable of the path 
		inputPath = inputPath.split('/')#splitting up the path with a '/'
		inputFile = inputPath[-1]#gets the last file/directory of the path 
		data, server_address = clientData.recvfrom(buf) #waiting to recieve data

		with open(data, 'wb') as file_to_write:#opens file and writes bytes as a file_to_write
			try:
			    while(data):#while there is data
			        file_to_write.write(data)#write to the file  
			        clientData.settimeout(2)
			        data,server_address = clientData.recvfrom(buf)#waiting to recieve data
			except timeout:#timeout exception
			    file_to_write.close()
			    print "File Downloaded"
		print('get successful')
	else:

		#for ls and cd
		clientControl.send(bytes(command.encode('utf-8')))#sends commands
		messageControl = clientControl.recv(512)#gets information back from server
		messageControl = messageControl.decode('utf-8')#decodes it
		print(messageControl)#shows it



