#!/usr/bin/env python
#---------------------------------------------------------------------
# regserver.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

# single command-line arg 
# reg + regserver must be running on different computers
# if command arg is incorrect, then regserver must write descriptive 
# error message to stderr and exit 

from sys import exit, argv
from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

#---------------------------------------------------------------------
# mangela

# connect to a port 
def main(argv): 

	BACKLOG = 5 

	if len(argv) != 2: 
		print('%s port' % argv[0])
		exit(1)
	try: 
		port = int(argv[1])
		serverSock = socket(AF_INET, SOCK_STREAM)
		print('Opened server socket')
		serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		serverSock.bind(('', port))
		print('Bound server socket to port')
		serverSock.listen(BACKLOG)
		print('Listening')
		while True:
			try:
				sock, clientAddr = serverSock.accept()
				print('Accepted connection for ' + str(clientAddr))
				print('Opened socket for ' + str(clientAddr))
				handleClient(sock, clientAddr)
				sock.close()
				print('Closed socket for ' + str(clientAddr))
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
