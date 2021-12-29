import socket
from pythonosc import udp_client

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ipAdress = '.'.join(get_ip().split('.')[:-1] + ["255"])
client = udp_client.SimpleUDPClient(ipAdress, 8000)
client.send_message("/filter", 9999)
