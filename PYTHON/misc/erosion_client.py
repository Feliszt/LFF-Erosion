import socket

hote = "192.168.1.255"
port = 9000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(port))

print("Close")
socket.close()
