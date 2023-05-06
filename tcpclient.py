import socket
import threading
from string import ascii_uppercase
def getChoice():
    print("I want to: ")
    print("1. Join a room")
    print("2. Create a room")
    choice = input(">>")
    if choice == '1' or choice == '2':
        return choice
    else:
        return getChoice()
    



username = input('Enter a username to chat. This name will apppear in the chat: ')
choice = getChoice() # 1 join a room 2 create a room
roomID = ''

if(choice == '1'):
    roomID = input("Enter room ID to join: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1' ,55555))
def receive():
    while True:
        try:
            message= client.recv(1024).decode('ascii')
            if message == 'key':
                client.send(f'{choice}:{roomID}:{username}'.encode('ascii'))
            elif message == 'invalidRoomID':
                print('No room with that ID')
                client.close()
                break
            else:
                print(message) 
        except:
            print('You left the chat!')
            client.close()
            break

def write():
    while True:
        message = input("")
        if(message == 'exitroom()'):
            client.close()
            break
        message = f'{username}:{message}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

   