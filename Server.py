import socket
import threading
import sys
import time
from test import Snake
import pickle
import random
from move import Move

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connections = []
sock.bind(('192.168.0.102', 10000))
sock.listen(1)
snakes = {"apples": [] }
colors = ["red","green","blue","yellow","brown","orange"]
scale = 10


def mainloop():
    while True:
        for connection in connections:
                try:

                    connection.send(pickle.dumps(snakes))
                except:
                    connection.close()
                    continue
        time.sleep(0.1)


def rand_position(snake):
    snake.x = random.randint(0,500/scale -1)*scale
    snake.y = random.randint(0,500/scale -1)*scale
    col = random.randint(0,5)
    snake.direction = 3
    snake.color = colors[col]
    return snake

def handler(c, a):
    while True:
        try:
            data = c.recv(2048)
            data = pickle.loads(data)
            if data[0].direction == 0:
                data[0] = rand_position(data[0])
                snakes[data[0].ids] = data
                c.send(pickle.dumps(snakes))
            else:
                snakes[data[0].ids] = data
        except:
            continue
        if not data:
            print("no data!")
            break

snakes["apples"].append(Snake(40,40,999,"red",5))
print("Server start")
aThread = threading.Thread(target=mainloop)
aThread.daemon = True
aThread.start()


while True:
    try:
        c, a = sock.accept()
        cThread = threading.Thread(target=handler, args=(c, a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)
        print('connection from : ', a)
    except:
        continue


