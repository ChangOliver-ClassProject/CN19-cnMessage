import threading
import hashlib
import pickle
import select
import socket
import time
import sys
import os

from util import *
from encryption import *
import newMessageDetector


def recvall(sock, timeout=1.5):
    sock.setblocking(0)
    total_data = []; data = ''; begin = time.time()
    while 1:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            data = sock.recv(8192)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return b''.join(total_data)


class Thread_Controller():
    def __init__(self, _sock, _user, _recepient): 
        self._running = True
        self._lock = False
        self._sock = _sock
        self._user = _user
        self._recepient = _recepient
        self.messageDetector = newMessageDetector.newMessageDetector(self._sock, self._user, self._recepient)

    def terminate(self): 
        self._running = False
      
    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False

    def islocked(self):
        return self._lock

    def run(self, sock): 
        while self._running: 
            readable, writable, exceptional = select.select([sock], [], [sock])
            if (sock in readable):
                data = recvall(sock)
                if not data:
                    continue
                recv_pkt = pickle.loads(data)
                if (recv_pkt.identifier == 000):
                    print(colored("Closing session...", NOTIFY_col))

                elif (recv_pkt.identifier == 301):
                    if (recv_pkt.content[0] != True and recv_pkt.content[0] != False): # recipient
                        print(colored("\nYou recieve a file", NOTIFY_col, attrs=[NOTIFY_attr]))
                        print(colored("Input: ", THEME_col, attrs=[THEME_attr]))
                        with open(recv_pkt.content[0], mode="wb") as f:
                            try:
                                f.write(recv_pkt.content[1])
                                print(colored("Write file Successfully", SUCCESS))
                            except Exception as e:
                                print(colored("Write File:" + str(e), ERROR))
                                exit(0)


                elif (recv_pkt.identifier == 302 and recv_pkt.content[0] == True):
                    with open(self.messageDetector.log_name, mode="wb") as logf:
                        for i in range(len(recv_pkt.content[1])):
                            logf.write(recv_pkt.content[1][i])

                    key_path = decide_filename(self._user, self._recepient)
                    with open(key_path, mode="rb") as f:
                        AES_key = f.read()

                    message = AES_decrypt(recv_pkt.content[1], AES_key)
                    print(colored(message, CONTENT))
                    self.unlock()
