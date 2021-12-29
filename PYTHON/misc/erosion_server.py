import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('192.168.1.19', 9000))

while True:
        socket.listen(5)
        client, address = socket.accept()
        print("{} connected".format(address))

        response = client.recv(255)
        if response != "":
                print(response)

print("Close")
client.close()
stock.close()
