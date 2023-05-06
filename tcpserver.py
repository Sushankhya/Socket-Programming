import threading
import socket
from string import ascii_uppercase
import random
host = '127.0.0.1' #localhost
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

rooms = [ChatRoom('GLOBAL')]

def handle(room, client):
    while True:
        try:
            message = client.recv(1024) #1024 bytes
            room.displayAll(message)
        except:
            room.removeClient(client)
            break


def generateRoomID():
    while True:
        match_id = False
        roomid = ''
        for _ in range(5):
            roomid += random.choice(ascii_uppercase)
        for room in rooms:
            if room.roomID == roomid:
                match_id = True
                break
        if not match_id:
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
        choice, roomid, username = client.recv(1024).decode('ascii').split(':')
        #choice = 2 means user wants to create a 
        if(choice == '2'):
            newRoomID = generateRoomID()
            rooms.append(ChatRoom(newRoomID))
            roomid = newRoomID
            client.send(f'Created room. Room id is {roomid}'.encode('ascii'))

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






