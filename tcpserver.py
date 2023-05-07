import os
import socket

host = '172.17.0.60'
port = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host ,port))
server_socket.listen()
print('Server is listening....')

client_socket, client_address = server_socket.accept()

file_contents = client_socket.recv(1024).decode()

file = open('receivedFile.txt', "w")
file.write(file_contents)
file.close()
# print(file_contents)
print("File received....")

# close the socket
client_socket.close()
server_socket.close()
