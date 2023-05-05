import threading
import socket

host = '192.168.137.1'#'127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
usernames= []

def displayAll(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024) #1024 bytes
            displayAll(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            #getting failed connection of client's index
            username = usernames[index]
            displayAll(f'{username} has left the chat!'.encode('ascii'))
            usernames.remove(username)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('key'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        clients.append(client)
        usernames.append(username)
        print(f'Username of client is {username}')
        displayAll(f'{username} joined the chat'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle,args= (client,))
        thread.start()

print('Server is listening')
receive()






