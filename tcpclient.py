import socket
import threading

username = input('Enter a username to chat. This name will apppear in the chat/n')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.137.1' ,55555))

def receive():
    while True:
        try:
            message= client.recv(1024).decode('ascii')
            if message == 'key':
                client.send(username.encode('ascii'))
            else:
                print(message) 
        except:
            print('Error occured!!!')
            client.close()
            break

def write():
    while True:
        message = f'{username}:{input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

   