import socket

hote = "192.168"
port = 9000

for i in range(0, 2) :
    for j in range(0, 256) :
        ip = hote + ".{}.{}".format(i, j)

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((ip, port))

        try :
            socket.send("hello")
        except:
            print("not connected to {}".format(ip))

c = """

print("Connection on {}".format(port))

print("Close")
socket.close()
"""
