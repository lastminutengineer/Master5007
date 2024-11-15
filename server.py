#!/usr/bin/env python3
import socket
import threading
# connection data
host = '127.0.0.1'
port = 55555
# start server 
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # socket.AF_INET tells python  to use ipv4 addresses ; socket.SOCK_STREAM specifies TCP protocols
server.bind((host,port)) # bind the server and host
server.listen() # starts listening & server.listen is inbuild socket module object (we dont need to define specifically)
# List for clients and nickname
clients =[]
nicknames=[]
# sending messages to all connected clients
def broadcast(message) : # broadcast is a function that sends messages to all clients
    for client in clients :
        client.send(message)
# handling messages from clients
def handle (client): # for handling communication between server and client 
    while True : # to run infinite loop as long as server is manually off
        try :
            # for broadcasting the message
            message = client.recv(1024) # broadcasting the message by calling the fuction ; client.recv is inbuild and allows size of 1024 bytes
            broadcast(message) # brodcast message means it sends messages to clients
        except : 
        # for removing and closing the clients
            index= clients.index(client)# clients.indext(clients) : index finds the position of clients in clients list (it is because when we want to remove client we have to remove nickname also )
            clients.remove(client)
            client.close()
            nickname = nicknames[index] 
            broadcast('{} left !'.format(nickname).encode('ascii')) # we encode because over a network he data should be in binary form not in plain text so we use 'ascii'
            nickname.remove(nickname) # 
            break 
def recieving () : # handles incoming client connections
    # accepting connections
    while True :
    # requests and store nicknames :
        client,address = server.accept()      # server.accept() waits for a client to connect to the server
        print("Connected with{}".format(str(address)))
        client.send('NICK'.encode('ascii') )  # sends NICK prompt from server to client and requests to enter nickame (in client side scrpit we will define if nick is send you have to enter nick name , so dont worry about this)
        nickname = client.recv(1024).decode('ascii')            # server waits for client response with nickname ;
        nicknames.append(nickname)                              # appends that nickname to nicknames list
        print("Connected with {}".format(nickname))             # print and broadcast nickname of client in server console basically for logging purpose
        broadcast("{} joined!".format(nickname).encode('ascii'))# broadcasts the message to all connected clients notifying new client is joined
        client.send('connected to server!'.encode('ascii'))     # message is send to client from server after recieving the connection and storing the nicknames
    # handling the thread for client :
        thread = threading.Thread(target=handle, args=(client,)) # (target = handle , args=(client,)) thread now start handling communication with client
        thread.start()                                           # without threads server will be able to handle one client only; so we use threads to handle multiple clients concurrently 
