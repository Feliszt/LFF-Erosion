# network / OSC
from pythonosc import udp_client
from pythonosc import osc_message_builder
from pythonosc import dispatcher
from pythonosc import osc_server
import socket
# threading
import threading
# utils
import time
import json
import itertools
import asyncio
import random
import math

# wrapper for osc messages
def send_osc_message(_osc_client, _address, *arg) :
    msg = osc_message_builder.OscMessageBuilder(address = _address)
    for el in arg :
        msg.add_arg(el[0], arg_type=el[1])
    msg = msg.build()
    _osc_client.send(msg)
    return

# launch thread for function
def launch_thread(_function) :
    thread = threading.Thread(target = _function)
    thread.daemon = True
    thread.start()

# get ip of machin on network
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
