#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


LOGIN_STATE = 1
CHAT_ROOM_SELECT_STATE = 2 
CHAT_STATE = 3

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    
    StepNum = 0
    name = client.recv(BUFSIZ).decode("utf8")
    
    ClientState = CHAT_ROOM_SELECT_STATE
    
    ChatRoom = None
    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            x = [ChatRooms[ChatRoom].remove((client,_tempname)) for (client,_tempname) in ChatRooms[ChatRoom] if _tempname == name ]
            broadcast(bytes("%s has left the chat." % name, "utf8"),"",ChatRoom)
            break
        else :
            if(ClientState == LOGIN_STATE):
                if(StepNum == 0):
                    #Receive ClientCertificate
                    #Verify Certificate, Generate Nonce and encrypt with Client Public Key
                    #Sends Server Certificate and Nonce encrypted with Client Public Key
                    StepNum+=1
                elif(StepNum == 1):
                    #Receive Server Nonce Response, Client Nonce encrypted with Server Public Key
                    #Check Server Nonce equality, Decrypt Client Nonce with Server Private Key
                    #Sends Client Ticket encrypted with Client Public Key, and Client Nonce
                    StepNum+=1
                else:
                    #There is an error
                    pass
            elif(ClientState == CHAT_ROOM_SELECT_STATE):
                if(StepNum == 2 ):
                    #Receives Client Ticket, timestamp, ChatroomName
                    #Decrypt it with Server private key
                    #Sends ChatRoom Key encrypted with Client Public Key
                    StepNum+=1
                else:
                    #There is an error
                    pass
                ChatRoom = msg.decode("utf8")
                welcome = 'Welcome %s in Chat Room : %s! If you ever want to quit, type {quit} to exit.' % (name,ChatRoom)
                client.send(bytes(welcome, "utf8"))
                if ChatRoom not in ChatRooms.keys(): 
                    ChatRooms[ChatRoom] = []
                ChatRooms[ChatRoom].append((client,name))
                msg = "%s has joined the chat!" % name
                broadcast(bytes(msg, "utf8"),"",ChatRoom)
                ClientState = CHAT_STATE
            elif ClientState == CHAT_STATE:
                if(StepNum == 3):
                    #Receives Client message encrypted with Chatroom key
                    #Decrypt it with ChatRoom key
                    #Calc checksum
                    #Send Message and CheckSum with encrypted with Chat room Key
                    StepNum+=1
                broadcast(msg, name+": ",ChatRoom)
                
            

        


def broadcast(msg, prefix="",ChatRoom=None):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock,name in ChatRooms[ChatRoom]:
        sock.send(bytes(prefix, "utf8")+msg)


ChatRooms = {}
addresses = {}


HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
#Load Server Certificate
#Load Server Private Key
#Load Server Private Key

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()