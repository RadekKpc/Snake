import socket
import sys
import pickle

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.102', 10001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

ids = 2
adresy = []

while True:
    # Wait for a connection
    print('Waiting for connection...')
    connection, client_address = sock.accept()
    try:
        print('connection from : ', client_address)

        idc = int(str(connection.recv(4),'utf8'))
        print("Przydzielam : ",str(ids))
        if not idc:
            connection.send(bytes(str(ids),'utf8'))
            print("przydzielono id: ", ids)
            ids = ids + 1
        # Receive the data in small chunks and retransmit it

            # data = connection.recv(1024)
            # data = pickle.loads(data)
            # x = data["x"]
            # y = data["y"]

            # print("data : ",data["x"])
    except:
        continue
# Clean up the connection

connection.close()