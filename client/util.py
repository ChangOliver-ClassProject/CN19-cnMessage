import threading
import hashlib
import pickle
import socket
import time
import sys
import os

from termcolor import colored

THEME_col = 'yellow'
THEME_hi = 'on_blue'
THEME_attr = 'bold'

NOTIFY_col = 'white'
NOTIFY_attr = 'blink'

ERROR = 'red'
SUCCESS = 'cyan'
CONTENT = 'blue'

SERVER_IP = '140.112.30.125'
PORT = 20205
RECV_SIZE = 10485761

class packet():
    def __init__(self, _identifier, _content):
        self.identifier = _identifier
        self.content = _content
