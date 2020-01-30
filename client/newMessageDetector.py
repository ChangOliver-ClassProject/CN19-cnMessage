import threading
import pickle
import socket
import time
import sys
import os

from util import *

def decide_filename(user, recipient):
    if user < recipient:
        return 'local_cache/log/' + user + '_' + recipient + '.log'
    else:
        return 'local_cache/log/' + recipient + '_' + user + '.log'


class newMessageDetector():
    def __init__(self, _sock, _user, _recipient):
        self.sock = _sock
        self.user = _user
        self.recipient = _recipient
        self.log_name = decide_filename(self.user, self.recipient)
        
        self.sock.sendall(pickle.dumps(packet(302, [self.user, self.recipient])))
        recv_pkt = pickle.loads(self.sock.recv(RECV_SIZE))
        if (recv_pkt.content[0] == "False"): # There has no log on the server yet
            self.hasNewMessage = False
        elif (not os.path.exists(self.log_name)):
            server_log = recv_pkt.content[1]
            # True if server_log is not empty
            self.hasNewMessage = True if server_log else False
        else:
            with open(self.log_name, mode="rb") as f:
                local_log = [line for line in f.readlines()]
            server_log = recv_pkt.content[1]
            # print(server_log)
            # print(local_log)

            self.hasNewMessage = (local_log != server_log)   

