# SecureChatRoom Application Using Python


# Python Packages

tkinter
 
cryptograpy 

# Description

This a secure chat room application.
Public Key Cryptography is used while initializing the connection and
Symmetric Key Cryptography is used while messaging between clients.

This is made up of 

server side code(server.py), 

client side code(client.py), 

certification authority an cerficicate generator code(ca.py)


# How to Use 
  
  First, run ca.py to generate certification authority, chat server, clients. 
  Now you have public and private key pairs, user passwords and certificates in seperate files.
  
  Second, place these files in appopriate folders to run client.py and server.py(For example, client0 should place its key files, password file and ca public key file into same directory with client.py )
  
  Third, run client.py and server.py.
