import socket

# define the server's IP address and port number
host = '172.17.0.60'
port = 55555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host,port))


# specify the file to transfer
filename = 'impfile.txt'

# open the file and read its contents
with open(filename, 'r') as f:
    file_contents = f.read()

# send the file contents to the server
client_socket.send(file_contents.encode())

# close the socket
client_socket.close()
