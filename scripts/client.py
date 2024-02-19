import socket
from threading import Thread

nickname = input('Enter your nickname: ')

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread: break
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except Exception as e:
            print(f'Error occurred: {e}')
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        msg = f'{nickname}: {input("")}'
        client.send(msg.encode('utf-8'))

rec_thread = Thread(target=recieve)
rec_thread.start()

write_thread = Thread(target=write)
write_thread.start()