import socket
import sys
import pickle
from tkinter import *
import time
from test import Snake
from move import Move

window = Tk()
window.title("SNAKE - ONLINE")
window.geometry("500x500")
canvas = Canvas(window,width=500,height=500)
canvas.place(x=0,y=0)
canvas.create_rectangle((0,0,500,500),fill ="#ffffff")
scale = 10
ids = 0
direction = 0
my_snake = []
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.102', 10001)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

while True:

    try:

         # Send data
        if not ids:
            print('sending {!r}'.format(ids))

            sock.send(bytes(str(ids),'utf8'))
            data = sock.recv(4)
            ids = int(str(data,'utf8'))
            print("Przydzielono id " , ids)
        # Look for the response

    finally:
        if ids:
            break
print('closing socket')
sock.close()

#Game Server

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Connect to Server...")
sock.connect(('192.168.0.102', 10000))
print("Connect successful")
sock.send(pickle.dumps([Snake(50,50,ids,"blue",0)]))
data = sock.recv(1024)
data = pickle.loads(data)
my_snake = data[ids]
direction = my_snake[0].direction
my_snake.append(Snake(my_snake[0].x-10,my_snake[0].y,ids,my_snake[0].color,3))
my_snake.append(Snake(my_snake[0].x-20,my_snake[0].y,ids,my_snake[0].color,3))
my_snake.append(Snake(my_snake[0].x-30,my_snake[0].y,ids,my_snake[0].color,3))
print(my_snake)
#KEYBOARD

def move(direction):

    for i in range(len(my_snake)-1,0,-1):
        my_snake[i].x = my_snake[i-1].x
        my_snake[i].y = my_snake[i-1].y

    if direction == 1:
        my_snake[0].x = my_snake[0].x - scale
    if direction == 2:
        my_snake[0].y = my_snake[0].y - scale
    if direction == 3:
        my_snake[0].x = my_snake[0].x + scale
    if direction == 4:
        my_snake[0].y = my_snake[0].y + scale
    if my_snake[0].x == 500:
        my_snake[0].x = 0
    if my_snake[0].y == 500:
        my_snake[0].y = 0
    if my_snake[0].x == -10:
        my_snake[0].x = 490
    if my_snake[0].y == -10:
        my_snake[0].y = 490

    for a in apple:
        if my_snake[0].x == a.x and my_snake[0].y == a.y:
            my_snake.append(Snake(-10,-10,ids,my_snake[0].color,direction))


def left(event):
    global direction
    if direction != 3:
        direction = 1
def right(event):
    global direction
    if direction != 1:
        direction = 3
def up(event):
    global direction
    if direction != 4:
            direction = 2
def down(event):
    global direction
    if direction != 2:
        direction = 4


x = window.bind("a", left)
x = window.bind("w", up)
x = window.bind("d", right)
x = window.bind("s", down)

#MAIN LOOP
while True:
    try:
        window.update_idletasks()
        window.update()
        data = sock.recv(2048)
        data = pickle.loads(data)
        sock.send(pickle.dumps(my_snake))
        apple = data["apples"]

        canvas.create_rectangle((0,0,500,500),fill ="#ffffff")
        for key, snake2 in data.items():
            for snake in snake2:
                canvas.create_rectangle((snake.x,snake.y,snake.x + 10,snake.y + 10),fill=snake.color)
        move(direction)
        time.sleep(0.01)

    except:
        continue


sock.close()
