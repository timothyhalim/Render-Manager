import string
import random
import os
import socket

def get_host():
    return socket.gethostname()

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def get_username():
    return os.getlogin()

def code_generator(chars=4):
    strings = string.ascii_letters + string.digits
    code = str('').join([random.choice(strings) for i in range(chars)])
    return code