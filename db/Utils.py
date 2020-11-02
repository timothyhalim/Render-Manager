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

def convert_second(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return f"{int(day)} Day, {int(hour)}:{int(minutes)}:{int(seconds)}"