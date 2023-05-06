import threading
import socket
from string import ascii_uppercase
import random
host = '192.168.202.21'#'127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

class ChatRoom:
    def __init__(self, roomID):
        self.roomID = roomID
        self.clients = []
        self.usernames = []
    
    def displayAll(self, message):
        for client in self.clients:
            client.send(message)

    def addClient(self, client, username):
        self.clients.append(client)
        self.usernames.append(username)
        self.displayAll(f'{username} joined the room.'.encode('ascii'))

    def removeClient(self, client):
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        leftUsername = self.usernames[index]
        self.displayAll(f'{leftUsername} has left the chat!'.encode('ascii'))
        self.usernames.pop(index)


def handle(room, client):
    while True:
        try:
            message = client.recv(1024) #1024 bytes
            room.displayAll(message)
        except:
            room.removeClient(client)
            break

rooms = [ChatRoom('ABCDE'), ChatRoom('12345')]

def generate_room_ID():
    while True:
        roomid = ''
        for _ in range(5):
            roomid += random.choice(ascii_uppercase)
        for room in rooms:
            if room.roomID == roomid:
                break
    return roomid

def getRoomFromID(roomid):
    for room in rooms:
        if room.roomID == roomid:
            return room

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('key'.encode('ascii'))
        roomid, username = client.recv(1024).decode('ascii').split(':')

        # if(choice == '2'):
        #     newRoomID = generate_room_ID()
        #     rooms.append(ChatRoom(newRoomID))
        #     roomid = newRoomID

        room = getRoomFromID(roomid)

        if(not room):
            client.send('invalidRoomID'.encode('ascii'))
            continue

        room.addClient(client, username)
        print(f'Username of client is {username}: ROOM - {room.roomID}')
        thread = threading.Thread(target=handle,args= (room, client))
        thread.start()

print('Server is listening')
receive()






