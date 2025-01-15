import random
import socket
from threading import Thread

colors_cells = [
    (80, 252, 54), (36, 244, 255), (243, 31, 46),
    (4, 39, 243), (254, 6, 178), (255, 211, 7),
    (216, 6, 254), (145, 255, 7), (7, 255, 182),
    (255, 6, 86), (147, 7, 255)
]

dots = {j: {'x': random.randint(20, 1980), 'y' : random.randint(20, 1980), 'color' : colors_cells[random.randint(0, len(colors_cells)-1)]} for j in range(2000)}

all_users = {}

def upd_eaten(dots, all_users):
    eaten_dots_ids = []
    for i, dot in dots.items():
        for name, user in all_users.item():
            if ((dot['x'] - user['x'])**2 + (dot['y'] - user['y'])**2)**0.5 <= user['mass']/2:
                all_users[name]['mass'] += 0.5
                eaten_dots_ids.append(i)

    for dot in eaten_dots_ids:
        del dots[dot]
    return eaten_dots_ids

def on_new_client(clientsocket, addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg == b'close':
            break
        if msg == b'spawn':
            msg = bytes(str(dots), encoding='UTF-8')
            clientsocket.sendall(msg)
            print('sent dots')
        else:
            user = eval(msg.decode('UTF-8'))
            all_users[user['name']] = user
            eaten_dots_ids = upd_eaten(dots, all_users)
            resp = {'user': all_users[user['name']], 'eaten_dots_ids': eaten_dots_ids}
            msg = bytes(str(resp), encoding='UTF-8')
            clientsocket.send(msg)
    clientsocket.close()

host = 'localhost'
port = 34325
SERVER_ADDRESS = (host, port)
s = socket.socket()
s.bind(SERVER_ADDRESS)
s.listen(10)
print('Server started!')
print('Waiting for clients...')

try:
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        thread = Thread(target=on_new_client,args=(c, addr))
        thread.start()
except KeyboardInterrupt:
    s.close()
    print('server closed')
