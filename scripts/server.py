import socket
from threading import Thread
import requests

def get_public_ip():
    try:
        response = requests.get("https://ifconfig.co/ip")
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        return None

public_ip = get_public_ip()
if public_ip:
    print(f"Public IP Address: {public_ip}")
else:
    print("Failed to fetch public IP address.")

#this will connect to a server i will have setup on an old laptop and running ubuntu server off of
HOST = '153.91.233.189'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            broadcast(client.recv(1024))
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('f{nickname} left the chat'.encode('utf-8'))
                nicknames.remove(nickname)
                break
def recieve():
    while True:
        client, addr = server.accept()
        print('Connected by', str(addr))

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname: {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('utf-8'))
        client.send('Connected to server'.encode('utf-8'))

        thread = Thread(target=handle, args=(client,))
        thread.start()

print('server is listening')
recieve()