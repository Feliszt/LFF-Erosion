from pythonosc import dispatcher
from pythonosc import osc_server
import socket

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

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/filter", print)

server = osc_server.ThreadingOSCUDPServer((get_ip(), 8000), dispatcher)
server.serve_forever()
